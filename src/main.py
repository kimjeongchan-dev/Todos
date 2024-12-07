from fastapi import Depends, FastAPI, Body, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo
from database.repository import get_todos


app = FastAPI()

@app.get("/todos", status_code=200)
def get_todos_handler(order: str | None = None, db: Session = Depends(get_db)):
    todos: list[Todo] = get_todos(db)
    if order == "DESC":
        return todos[::-1]

    return todos


