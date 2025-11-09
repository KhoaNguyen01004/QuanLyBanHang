import os
from datetime import datetime, UTC

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send

from app.api import users, carts, items
from app.core.config import settings
from app.db.db import engine, Base, SessionLocal
from app.models.item import Item

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
# Determine environment (production vs. development)
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Add SessionMiddleware with secure settings in production
def get_session_middleware_settings():
    if DEBUG:
        return dict(secret_key=settings.secret_key, same_site="lax", https_only=False)
    else:
        # Railway/production: secure cookies
        return dict(secret_key=settings.secret_key, same_site="lax", https_only=True)

app.add_middleware(SessionMiddleware, **get_session_middleware_settings())

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
    db = SessionLocal()
    from app.services.shop_services import get_user, get_user_by_username_or_email, get_or_create_cart

    try:
        user_id = None
        session_id = None
        if username:
            # Try to resolve the session username to a DB user (could be stored as id or username/email)
            resolved_user = get_user(db, username)
            if not resolved_user:
                resolved_user = get_user_by_username_or_email(db, username)
            if resolved_user:
                user_id = resolved_user.id
        # If no user_id, attempt to use or create a session_id stored in the server session
        if not user_id:
            session_id = request.session.get('session_id')
            if not session_id:
                import uuid
                session_id = uuid.uuid4().hex
                request.session['session_id'] = session_id

        cart = get_or_create_cart(db, user_id=user_id, session_id=session_id)
        if cart:
            # cart.items is the relationship on the Cart model
            for cart_item in cart.items:
                item = cart_item.item
                if not item:
                    continue
                # Normalize picture path similar to home view
                pic_path = item.picture_path or ''
                if pic_path.startswith('images/'):
                    final_path = pic_path
                elif pic_path.startswith('/static/images/'):
                    final_path = pic_path[len('/static/'):]
                elif pic_path:
                    final_path = f"images/items/{pic_path}"
                else:
                    final_path = "images/items/default.png"

                items.append({
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "price": item.price,
                    "quantity": cart_item.quantity,
                    "picture_path": final_path,
                    "tags": item.tags.split(",") if item.tags else [],
                })
    finally:
        db.close()

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

# Export asgi_app for Uvicorn (ensures all middleware is applied)
asgi_app = app

# IMPORTANT: For session and custom middleware to work, run with:
# uvicorn app.main:asgi_app --reload
# NOT uvicorn app.main:app --reload

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(asgi_app, host="0.0.0.0", port=port)
