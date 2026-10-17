from fastapi import FastAPI, Request, WebSocket, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

# 静的ファイルフォルダのマウント
app.mount("/static", StaticFiles(directory="static"), name="static")
#app.mount("/my-solid-element-app", StaticFiles(directory="my-solid-element-app"), name="solid")
app.mount("/solid", StaticFiles(directory="my-solid-element-app"), name="solid-element")

# テンプレートの設定
templates = Jinja2Templates(directory="templates")


# 【解決策】古い環境でもHTML側の「url_for('static', filename='xxx')」を動かすためのカスタム関数
def custom_url_for(name: str, **path_params):
    # HTML内の 'filename' を FastAPI の仕様であるパスパラメータ（path）に変換する
    if name == 'static' and 'filename' in path_params:
        path_params['path'] = path_params.pop('filename')
    return app.url_path_for(name, **path_params)

# カスタム関数をJinja2のグローバル関数として上書き登録
templates.env.globals['url_for'] = custom_url_for


# 接続しているWebSocketクライアントの管理クラス
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()



# 1. 最初アクセスした時の「名前入力画面」
@app.get("/", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 2. 入力された名前を受け取り、チャット画面へリダイレクトする
@app.post("/login")
async def post_login(username: str = Form(...)):
    # URLのパラメータにユーザー名を乗せてチャット画面へ移動
    return RedirectResponse(url=f"/chat?username={username}", status_code=303)

# 3. 実際のチャット画面（ここで設定されたusernameをテンプレートに渡す）
@app.get("/chat", response_class=HTMLResponse)
async def get_chat(request: Request, username: str = "ゲスト"):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "username": username}
    )

"""
# Jinja2 テンプレートを表示する通常のエンドポイント
@app.get("/")
async def get(request: Request):
    # 例としてダミーのユーザー名や部屋IDをJinja2経由で渡す
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "username": "User_" + str(id(request))[:4]}
    )
"""

# WebSocket エンドポイント
@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    # 参加通知を全員に送信
    await manager.broadcast(json.dumps({"user": "System", "text": f"{username} が参加しました。"}))
    try:
        while True:
            # クライアントからのメッセージを待機
            data = await websocket.receive_text()
            # 受信したメッセージを全員にそのまま転送
            await manager.broadcast(json.dumps({"user": username, "text": data}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # 退室通知を全員に送信
        await manager.broadcast(json.dumps({"user": "System", "text": f"{username} が退室しました。"}))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
