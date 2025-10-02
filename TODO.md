# Shop Management Webapp Implementation TODO

## 1. Dependencies and Environment Setup
- [x] Create requirements.txt with FastAPI, SQLAlchemy, Pydantic, psycopg2-binary, python-dotenv, uvicorn
- [x] Create .env file with Supabase database URL and other environment variables

## 2. Core Configuration
- [x] Implement app/core/config.py for application settings and environment variables

## 3. Database Setup
- [x] Implement app/db/db.py for SQLAlchemy engine, session, and Base configuration

## 4. SQLAlchemy Models
- [x] Convert app/models/item.py to SQLAlchemy Item model
- [x] Implement app/models/cart.py as SQLAlchemy Cart model
- [x] Implement app/models/cart_item.py as SQLAlchemy CartItem association model
- [x] Implement app/models/user.py as SQLAlchemy User model

## 5. Pydantic Schemas
- [x] Create app/schemas/__init__.py
- [x] Create app/schemas/item.py with ItemCreate, ItemUpdate, Item schemas
- [x] Create app/schemas/cart.py with Cart, CartItem schemas
- [x] Create app/schemas/user.py with User schemas

## 6. Business Logic Services
- [x] Implement app/services/shop_services.py with item and cart management functions

## 7. API Endpoints
- [x] Implement app/api/items.py with CRUD endpoints for items
- [x] Implement app/api/carts.py with cart management endpoints
- [x] Implement app/api/users.py with basic user endpoints

## 8. FastAPI Application
- [x] Implement app/main.py: FastAPI app creation, CORS, router inclusion

## 9. Testing
- [x] Update tests/test_everything.py with basic unit and integration tests

## 10. Documentation
- [x] Update README.md with setup, usage, and deployment instructions
