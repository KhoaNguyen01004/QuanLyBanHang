import os
import json
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.api import users, carts, items
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.db.db import engine, Base, SessionLocal
from app.core.config import settings
from app.models.item import Item
from datetime import datetime, UTC
from starlette.types import ASGIApp, Receive, Scope, Send
from typing import List
from app.websocket_manager import manager  # Import the WebSocket manager from the new module

# Create database tables
Base.metadata.create_all(bind=engine)

# Keep the FastAPI instance available as `app` so tests can override dependencies.
app = FastAPI(
    title="Shop Management API",
    description="A FastAPI application for managing shop items, carts, and users",
    version="1.0.0"
)

SESSION_TIMEOUT_SECONDS = 3600  # 1 hour

class AutoLogoutASGIMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            async def send_wrapper(message):
                await send(message)
            async def receive_wrapper():
                return await receive()
            request = Request(scope, receive_wrapper)
            try:
                session = request.session
                username = session.get("username")
                now = datetime.now(UTC).timestamp()
                last_activity = session.get("last_activity")
                if username:
                    if last_activity and now - last_activity > SESSION_TIMEOUT_SECONDS:
                        session.clear()
                        response = RedirectResponse(url="/", status_code=302)
                        await response(scope, receive, send)
                        return
                    else:
                        session["last_activity"] = now
            except Exception:
                pass
        await self.app(scope, receive, send)

# Add middlewares to the FastAPI instance (keeps app as FastAPI for tests)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, same_site="lax", https_only=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local dev, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(carts.router, prefix="/api/carts", tags=["carts"])
app.include_router(items.router, prefix="/api/items", tags=["items"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    username = request.session.get("username")
    db = SessionLocal()
    items = db.query(Item).all()
    # Convert items to dicts and split tags into lists
    items_dicts = []
    for item in items:
        # Ensure correct image path
        pic_path = item.picture_path or ''
        if pic_path.startswith('images/'):
            final_path = pic_path
        elif pic_path.startswith('/static/images/'):
            final_path = pic_path[len('/static/'):]
        elif pic_path:
            final_path = f"images/items/{pic_path}"
        else:
            final_path = "images/items/default.png"  # fallback image
        item_dict = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "stock": item.stock,
            "picture_path": final_path,
            "tags": item.tags.split(",") if item.tags else [],
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "updated_at": item.updated_at.isoformat() if item.updated_at else None,
        }
        items_dicts.append(item_dict)
    db.close()
    return templates.TemplateResponse(request, "home.html", {"username": username, "items": items_dicts})

@app.get("/cart")
async def cart(request: Request):
    username = request.session.get("username")
    items = []
    items_path = "static/data/items.json"
    if os.path.exists(items_path):
        with open(items_path, 'r') as f:
            items = json.load(f)
    return templates.TemplateResponse(request, "cart.html", {"username": username, "items": items})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/register")
def register_redirect():
    return RedirectResponse(url="/api/users/register", status_code=302)

@app.get("/login")
def login_redirect():
    return RedirectResponse(url="/api/users/login", status_code=302)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

connected_clients = []

@app.websocket("/ws/stock-updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in connected_clients:
                await client.send_text(data)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

# Create the ASGI app wrapper that applies auto-logout behavior for runtime.
asgi_app = AutoLogoutASGIMiddleware(app)

# IMPORTANT: For session and custom middleware to work, run with:
# uvicorn app.main:asgi_app --reload
# NOT uvicorn app.main:app --reload

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(asgi_app, host="0.0.0.0", port=port)
