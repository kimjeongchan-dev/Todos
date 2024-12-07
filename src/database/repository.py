from sqlalchemy.orm import Session
from sqlalchemy import select

from database.orm import Todo

def get_todos(db: Session) -> list[Todo]:
    return list(db.scalars(select(Todo)))
