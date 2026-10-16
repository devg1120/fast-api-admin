from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jinja2 import TemplateNotFound

app = FastAPI()

# 静的ファイルフォルダ（CSS/JS用）のマウント
app.mount("/static", StaticFiles(directory="static"), name="static")

# テンプレートの設定
templates = Jinja2Templates(directory="templates")


# 前回のJinja2互換性エラーを回避するためのカスタム関数
def custom_url_for(name: str, **path_params):
    if name == 'static' and 'filename' in path_params:
        path_params['path'] = path_params.pop('filename')
    return app.url_path_for(name, **path_params)

templates.env.globals['url_for'] = custom_url_for


# 汎用的なHTMLレンダリング関数
def render(template_name: str, context: dict, request: Request) -> HTMLResponse:
    context["request"] = request
    template = templates.env.get_template(template_name)
    html_content = template.render(context)
    return HTMLResponse(content=html_content, status_code=200)


# 現在のURLセグメント（ページの識別子）を取得するヘルパー関数
def get_segment(request: Request):
    try:
        segment = request.url.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None


# 1. トップページ（/）のルーティング
@app.get('/')
def index_root(request: Request):
    segment = get_segment(request)
    try:
        # Flaskの defaults={'path': 'index.html'} と同じ挙動を再現
        return render('home/index.html', {"segment": segment}, request=request)
    except TemplateNotFound:
        return render('home/page-404.html', {"segment": segment}, request=request)


# 2. 動的なパス（/<path>）のルーティング
# {path:path} と書くことで、階層のあるパス（例: users/profile）も丸ごと取得できます
@app.get('/{path:path}')
def index(request: Request, path: str):
    segment = get_segment(request)
    try:
        # 入力されたパスに合うHTMLを templates/home/ フォルダ内から探して表示
        return render(f'home/{path}', {"segment": segment}, request=request)
    except TemplateNotFound:
        # ファイルが見つからなければ404ページを表示
        return render('home/page-404.html', {"segment": segment}, request=request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
