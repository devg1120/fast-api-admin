from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 1. 静的ファイル（CSS/JS/画像）の設定
# /static/css/adminlte.min.css のようにアクセスできるようになります
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. テンプレートエンジンの設定
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def admin_dashboard(request: Request):
    # index.html用のデータ
    data = {
        "user_count": 1250,
        "sales_amount": "¥450,000"
    }

    # ★ここがテンプレートの {% for menu in sidebar_menu %} と連動します
    sidebar_menu = [
        {
            "name": "ダッシュボード",
            "icon": "fas fa-tachometer-alt",
            "url": "/",
            "children": []
        },
        {
            "name": "コンテンツ管理",
            "icon": "fas fa-copy",
            "url": "#",
            "children": [
                {"name": "記事一覧", "url": "/articles"},
                {"name": "カテゴリ設定", "url": "/categories"}
            ]
        }
    ]

    return templates.TemplateResponse(
        request=request,
        #name="index.html",
        name="base.html",
        context={
            "request": request,
            "data": data,
            "sidebar_menu": sidebar_menu  # ←これが渡っているか確認
        }
    )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

