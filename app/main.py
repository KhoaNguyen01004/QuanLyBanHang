import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.api.carts import router as carts_router
from app.api.items import router as items_router
from app.api.users import router as users_router
from app.db.db import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Shop Management API",
    description="A FastAPI application for managing shop items, carts, and users",
    version="1.0.0"
)

# Session middleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Include routers
app.include_router(
    items_router,
    prefix="/api/items",
    tags=["items"]
)

app.include_router(
    carts_router,
    prefix="/api/carts",
    tags=["carts"]
)

app.include_router(
    users_router,
    prefix="/api/users",
    tags=["users"]
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

from fastapi import Request

@app.get("/")
def read_root(request: Request):
    if request.session.get('username'):
        return RedirectResponse(url="/welcome", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.get("/welcome")
def welcome(request: Request):
    username = request.session.get('username')
    if not username:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("welcome.html", {"request": request, "username": username})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

from fastapi.responses import RedirectResponse

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
