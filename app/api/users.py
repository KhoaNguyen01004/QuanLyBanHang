from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.user import User, UserCreate
from app.services.shop_services import get_user, get_user_by_email, create_user
from app.core.security import verify_password
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(request: Request, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(db, email=form_data.username)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    if not verify_password(form_data.password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    # Set username in session
    request.session['username'] = user.username
    response = RedirectResponse(url="/welcome", status_code=303)
    return response


@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})


import unicodedata

@router.post("/register", response_class=HTMLResponse)
def register(request: Request, db: Session = Depends(get_db), username: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form("customer")):
    # Normalize and strip whitespace from password to avoid extra bytes
    password = unicodedata.normalize('NFC', password.strip())
    # Check password length for bcrypt limitation (72 bytes)
    if len(password.encode('utf-8')) > 72:
        error_msg = "Password cannot be longer than 72 bytes. Please choose a shorter password."
        return templates.TemplateResponse("register.html", {"request": request, "error": error_msg})
    # Check if user already exists
    db_user = get_user_by_email(db, email=email)
    if db_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email already registered"})
    # Create user
    user_create = UserCreate(username=username, email=email, password=password, role=role)
    create_user(db=db, user=user_create)
    # Redirect to login page after successful registration
    response = RedirectResponse(url="/login", status_code=303)
    return response


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/email/{email}", response_model=User)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists  
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)
