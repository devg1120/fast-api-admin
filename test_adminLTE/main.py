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

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    # ダッシュボードに渡したいデータがあれば辞書（context）に入れます
    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={"user_name": "管理者"}
    )

# 1. ダッシュボード (トップページ)
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request, "user_name": "管理者", "current_page": "dashboard"}
    )

# 2. ユーザー一覧ページ
@app.get("/users", response_class=HTMLResponse)
async def read_users(request: Request):
    # 本来はここでデータベースからユーザーリストを取得します
    dummy_users = [
        {"id": 1, "name": "山田 太郎", "email": "yamada@example.com", "role": "管理者"},
        {"id": 2, "name": "佐藤 花子", "email": "sato@example.com", "role": "一般ユーザー"},
    ]
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={"request": request, "users": dummy_users, "current_page": "users"}
    )

# 3. 商品一覧ページ
@app.get("/products", response_class=HTMLResponse)
async def read_products(request: Request):
    dummy_products = [
        {"id": 101, "name": "ノートPC", "price": 120000},
        {"id": 102, "name": "高機能マウス", "price": 8500},
    ]
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={"request": request, "products": dummy_products, "current_page": "products"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

