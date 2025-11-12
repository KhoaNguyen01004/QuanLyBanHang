import os
from datetime import datetime, UTC
import logging

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send

from app.api import users, carts, items, orders
from app.core.config import settings
from app.db.db import engine, Base, SessionLocal
from app.models.item import Item
from app.services.shop_services import get_user, get_user_by_username_or_email, get_or_create_cart
from app.utils.images import resolve_picture_path  # NEW import

# Create database tables
Base.metadata.create_all(bind=engine)

# Keep the FastAPI instance available as `app` so tests can override dependencies.
app = FastAPI(
    title="Shop Management API",
    description="A FastAPI application for managing shop items, carts, and users",
    version="1.0.0"
)

# Configure simple logging for startup messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.main")

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
# Allow overriding cookie SameSite via env var (COOKIE_SAMESITE), defaulting to 'lax'
COOKIE_SAMESITE = os.environ.get("COOKIE_SAMESITE", "lax").lower()

def get_session_middleware_settings():
    # Allow forcing insecure session cookies for local/dev testing via INSECURE_SESSIONS env var.
    # This keeps production behavior (https_only=True) unless DEBUG is True or INSECURE_SESSIONS is set.
    force_insecure = os.environ.get("INSECURE_SESSIONS", "0").lower() in ("1", "true", "yes")
    if DEBUG or force_insecure:
        return dict(secret_key=settings.secret_key, same_site=COOKIE_SAMESITE, https_only=False)
    else:
        # Railway/production: secure cookies
        return dict(secret_key=settings.secret_key, same_site=COOKIE_SAMESITE, https_only=True)

app.add_middleware(SessionMiddleware, **get_session_middleware_settings())

# Configure CORS origins from environment variable ALLOWED_ORIGINS
# - If ALLOWED_ORIGINS is provided (comma-separated), use that list (required when allow_credentials=True)
# - If not provided, keep the original wildcard for backward compatibility but log a warning
allowed_origins_env = os.environ.get("ALLOWED_ORIGINS", "").strip()
if allowed_origins_env:
    allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
else:
    allowed_origins = ["*"]
    logger.warning("ALLOWED_ORIGINS not set. Using wildcard '*' for CORS. When sending credentials (cookies), browsers will refuse credentials with '*' — set ALLOWED_ORIGINS to your frontend origin(s) for cookies to work in production.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # use env-driven list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log effective settings at startup (non-sensitive values only)
@app.on_event("startup")
def _log_startup():
    logger.info(f"Startup config: ALLOWED_ORIGINS={allowed_origins}, DEBUG={DEBUG}, INSECURE_SESSIONS={os.environ.get('INSECURE_SESSIONS','0')}, COOKIE_SAMESITE={COOKIE_SAMESITE}")

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(carts.router, prefix="/api/carts", tags=["carts"])
app.include_router(items.router, prefix="/api/items", tags=["items"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    username = request.session.get("username")
    db = SessionLocal()
    items = db.query(Item).all()
    # Convert items to dicts and split tags into lists
    items_dicts = []
    for item in items:
        final_path = resolve_picture_path(item.picture_path, item.name)
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

    # Resolve the logged-in user's email (if available) so the template can show it in the user menu
    email = None
    if username:
        try:
            resolved_user = get_user_by_username_or_email(db, username)
            if resolved_user:
                email = resolved_user.email
        except Exception:
            email = None

    db.close()
    return templates.TemplateResponse(request, "home.html", {"username": username, "email": email, "items": items_dicts})

@app.get("/cart")
async def cart(request: Request):
    username = request.session.get("username")
    items = []
    db = SessionLocal()

    try:
        user_id = None
        session_id = None
        if username:
            resolved_user = get_user(db, username)
            if not resolved_user:
                resolved_user = get_user_by_username_or_email(db, username)
            if resolved_user:
                user_id = resolved_user.id
        if not user_id:
            session_id = request.session.get('session_id')
            if not session_id:
                import uuid
                session_id = uuid.uuid4().hex
                request.session['session_id'] = session_id

        cart = get_or_create_cart(db, user_id=user_id, session_id=session_id)
        if cart:
            for cart_item in cart.items:
                item = cart_item.item
                if not item:
                    continue
                final_path = resolve_picture_path(item.picture_path, item.name)
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

@app.get("/checkout", response_class=HTMLResponse)
async def checkout(request: Request):
    # Keep it simple: server renders the shell; client will fetch and display latest cart.
    username = request.session.get("username")
    return templates.TemplateResponse(request, "checkout.html", {"username": username})

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

@app.get("/purchases", response_class=HTMLResponse)
async def purchases(request: Request):
    username = request.session.get("username")
    return templates.TemplateResponse(request, "purchases.html", {"username": username})

# Export asgi_app for Uvicorn (ensures all middleware is applied)
asgi_app = app

# IMPORTANT: For session and custom middleware to work, run with:
# uvicorn app.main:asgi_app --reload
# NOT uvicorn app.main:app --reload

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(asgi_app, host="0.0.0.0", port=port)
