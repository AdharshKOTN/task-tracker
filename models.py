from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    completed: bool = Field(default=False)
