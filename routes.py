from fastapi import APIRouter, Depends
from sqlmodel import select, Session
from models import Task
from database import get_session

router = APIRouter()

@router.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    return session.exec(select(Task)).all()

@router.post("/tasks")
def create_task(title: str, session: Session = Depends(get_session)):
    task = Task(title=title)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.post("/tasks/{task_id}/toggle")
def toggle_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task:
        task.completed = not task.completed
        session.commit()
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
    return {"message": "Task deleted"}
