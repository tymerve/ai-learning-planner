# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from routers import auth, plan
from models import Base
from database import engine

app = FastAPI()

# Statik ve template dosyaları
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

# Rotaları bağla
app.include_router(auth.router)
app.include_router(plan.router)

# Ana sayfa doğrudan login'e yönlendirir
@app.get("/")
async def root():
    return RedirectResponse("/login")

