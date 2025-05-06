# routers/plan.py
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import User, LearningPlan
from dotenv import load_dotenv
import google.generativeai as genai
import os
import re

router = APIRouter()
templates = Jinja2Templates(directory="templates")

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@router.get("/generate", response_class=HTMLResponse)
async def show_form(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/login")
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate_plan(request: Request, goal: str = Form(...), db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/login")

    model = genai.GenerativeModel("models/gemini-1.5-pro")
    prompt = (
        "I will provide you a learning goal. Please return a structured list of topics needed to achieve that goal,"
        " and assign an estimated number of weeks for each topic. Add 1-2 short informative sentences below each topic line.\n"
        "Respond only in this bullet point format:\n"
        "* Topic Name - X weeks\nShort description.\n"
        f"Goal: {goal}"
    )
    response = model.generate_content(prompt)
    plan = response.text

    matches = re.findall(r"[*\-–]\s*(.+?)\s*[-–]\s*(\d+)\s*weeks?", plan)
    topic_names = [m[0] for m in matches]
    durations = [int(m[1]) for m in matches]

    new_plan = LearningPlan(goal=goal, content=plan, user_id=int(user_id))
    db.add(new_plan)
    db.commit()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "goal": goal,
        "plan": plan,
        "topics": topic_names,
        "durations": durations
    })

@router.get("/my-plans", response_class=HTMLResponse)
async def list_plans(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/login")

    plans = db.query(LearningPlan).filter(LearningPlan.user_id == int(user_id)).all()
    return templates.TemplateResponse("myplans.html", {"request": request, "plans": plans})

@router.get("/my-plans/{plan_id}", response_class=HTMLResponse)
async def show_single_plan(plan_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/login")

    plan = db.query(LearningPlan).filter(LearningPlan.id == plan_id, LearningPlan.user_id == int(user_id)).first()
    if not plan:
        return RedirectResponse("/my-plans")

    matches = re.findall(r"[*\-–]\s*(.+?)\s*[-–]\s*(\d+)\s*weeks?", plan.content)
    topic_names = [m[0] for m in matches]
    durations = [int(m[1]) for m in matches]

    return templates.TemplateResponse("result.html", {
        "request": request,
        "goal": plan.goal,
        "plan": plan.content,
        "topics": topic_names,
        "durations": durations
    })

@router.post("/delete/{plan_id}")
async def delete_plan(plan_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    plan = db.query(LearningPlan).filter(LearningPlan.id == plan_id, LearningPlan.user_id == int(user_id)).first()
    if plan:
        db.delete(plan)
        db.commit()

    return RedirectResponse("/my-plans", status_code=302)

