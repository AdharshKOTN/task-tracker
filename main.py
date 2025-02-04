from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List
import os
from fastapi import FastAPI
from routes import router
from database import create_db_and_tables

app = FastAPI()

# Initialize database
create_db_and_tables()

# Include API routes
app.include_router(router)

# Database setup
DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, echo=True)

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    completed: bool = False

SQLModel.metadata.create_all(engine)

# Jinja templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root(request: Request, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/tasks")
def create_task(title: str, session: Session = Depends(get_session)):
    task = Task(title=title)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.post("/tasks/{task_id}/toggle")
def toggle_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task:
        task.completed = not task.completed
        session.commit()
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
    return {"message": "Task deleted"}