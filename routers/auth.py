# routers/auth.py

from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import User
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    response = RedirectResponse(url="/generate", status_code=status.HTTP_302_FOUND)
    response.set_cookie("user_id", str(user.id))
    return response


@router.get("/register")
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"})

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = User(username=username, password=hashed_pw)
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("user_id")
    return response
