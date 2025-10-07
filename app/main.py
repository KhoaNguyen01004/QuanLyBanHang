import os
import json
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.api import users, carts, items
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.db.db import engine, Base
from app.core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shop Management API",
    description="A FastAPI application for managing shop items, carts, and users",
    version="1.0.0"
)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
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
    # Render the public browsing homepage
    username = request.session.get("username")
    items = []
    items_path = "static/data/items.json"
    if os.path.exists(items_path):
        with open(items_path, 'r') as f:
            items = json.load(f)
    return templates.TemplateResponse("home.html", {"request": request, "username": username, "items": items})

@app.get("/cart")
async def cart(request: Request):
    username = request.session.get("username")
    items = []
    items_path = "static/data/items.json"
    if os.path.exists(items_path):
        with open(items_path, 'r') as f:
            items = json.load(f)
    return templates.TemplateResponse("cart.html", {"request": request, "username": username, "items": items})

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
