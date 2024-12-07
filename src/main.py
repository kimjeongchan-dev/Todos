from fastapi import Depends, FastAPI, Body, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo
from database.repository import get_todos
from schema.response import GetTodosResponse, TodoSchema


app = FastAPI()

@app.get("/todos", status_code=200)
def get_todos_handler(order: str | None = None, db: Session = Depends(get_db)) -> GetTodosResponse:
    todos: list[Todo] = get_todos(db)
    if order == "DESC":
        return GetTodosResponse(todos=[TodoSchema.from_orm(todo) for todo in todos[::-1]])

    return GetTodosResponse(todos=[TodoSchema.from_orm(todo) for todo in todos])


