from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.items import router as items_router
from app.api.carts import router as carts_router
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

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shop Management API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
