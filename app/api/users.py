from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.user import User, UserCreate
from app.services.shop_services import get_user, get_user_by_email, create_user, get_user_by_username_or_email
from app.core.security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse(request, "login.html", {})


@router.post("/login")
def login(request: Request, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    import logging
    user = get_user_by_username_or_email(db, identifier=form_data.username)
    if not user:
        logging.warning(f"Login failed: user not found for {form_data.username}")
        return templates.TemplateResponse(request, "login.html", {"error": "Invalid credentials"})
    if not verify_password(form_data.password, user.hashed_password):
        logging.warning(f"Login failed: invalid password for {form_data.username}")
        return templates.TemplateResponse(request, "login.html", {"error": "Invalid credentials"})
    # Set username in session
    request.session['username'] = user.username
    logging.warning(f"Login success: session after login: {dict(request.session)}")
    response = RedirectResponse(url="/", status_code=303)
    return response


@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse(request, "register.html", {"error": None})


import unicodedata

@router.post("/register", response_class=HTMLResponse)
def register(request: Request, db: Session = Depends(get_db), username: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form("customer")):
    # Normalize and strip whitespace from password to avoid extra bytes
    password = unicodedata.normalize('NFC', password.strip())
    # Check password length for bcrypt limitation (72 bytes)
    if len(password.encode('utf-8')) > 72:
        error_msg = "Password cannot be longer than 72 bytes. Please choose a shorter password."
        return templates.TemplateResponse(request, "register.html", {"error": error_msg})
    # Check if user already exists
    db_user = get_user_by_email(db, email=email)
    if db_user:
        return templates.TemplateResponse(request, "register.html", {"error": "Email already registered"})
    # Create user
    user_create = UserCreate(username=username, email=email, password=password, role=role)
    create_user(db=db, user=user_create)
    # Redirect to login page after successful registration
    response = RedirectResponse(url="/login", status_code=303)
    return response


@router.get("/{user_id}", response_model=User)
def read_user(user_id: str, db: Session = Depends(get_db)):
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


@router.post("/token")
def api_login_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username_or_email(db, identifier=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/debug/session")
def debug_session(request: Request):
    import logging
    session_data = dict(request.session) if hasattr(request, 'session') else 'No session'
    logging.warning(f"[DEBUG SESSION ENDPOINT] Session content: {session_data}")
    return {"session": session_data}
