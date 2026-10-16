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

# 共通のサイドバーメニュー定義（すべてのルーティングで使い回します）
SIDEBAR_MENU = [
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

# ① ダッシュボード (TOP画面)
@app.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    data = {"user_count": 1250, "sales_amount": "¥450,000"}
    return templates.TemplateResponse(
        request=request, 
        name="base.html", 
        context={"request": request, "data": data, "sidebar_menu": SIDEBAR_MENU}
    )

# ② 記事一覧画面（新設）
@app.get("/articles", response_class=HTMLResponse)
async def admin_articles(request: Request):
    # 本来はデータベース等から取得するサンプルデータ
    dummy_articles = [
        {"id": 1, "title": "FastAPIとAdminLTEの連携方法", "status": "公開中", "date": "2026-10-15"},
        {"id": 2, "title": "Bootstrap 5.3のCollapse機能を使いこなす", "status": "下書き", "date": "2026-10-14"},
    ]
    return templates.TemplateResponse(
        request=request, 
        name="articles.html",  # 新しいテンプレートファイル
        context={"request": request, "articles": dummy_articles, "sidebar_menu": SIDEBAR_MENU}
    )

# ③ カテゴリ設定画面（新設）
@app.get("/categories", response_class=HTMLResponse)
async def admin_categories(request: Request):
    dummy_categories = ["お知らせ", "テックブログ", "未分類"]
    return templates.TemplateResponse(
        request=request, 
        name="categories.html",  # 新しいテンプレートファイル
        context={"request": request, "categories": dummy_categories, "sidebar_menu": SIDEBAR_MENU}
    )





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

