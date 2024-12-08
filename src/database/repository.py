from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from database.orm import Todo, User
from schema.request import CreateTodoRequest, UpdateTodoRequest
from database.connection import get_db

class TodoRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db


    def get_todos(self) -> list[Todo]:
        return list(self.db.scalars(select(Todo)).all())

    def get_todo_by_todo_id(self, todo_id: int) -> Todo | None:
        return self.db.scalar(select(Todo).where(Todo.id == todo_id))

    def create_todo(self, request: CreateTodoRequest) -> Todo:
        todo = Todo(contents=request.contents, is_done=request.is_done)
        self.db.add(todo)
        self.db.flush()
        return todo

    def update_todo(self, todo: Todo, request: UpdateTodoRequest) -> Todo:
        todo.contents = request.contents
        todo.done() if request.is_done else todo.undone()
        self.db.flush()
        return todo


    def delete_todo(self, todo: Todo) -> None:
        self.db.delete(todo)
        self.db.flush()


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_user(self, name: str, password: str) -> User:
        user = User(name=name, password=password)
        self.db.add(user)
        self.db.flush()
        return user

    def get_user_by_name(self, name: str) -> User | None:
        return self.db.scalar(select(User).where(User.name == name))

    def get_user_by_user_id(self, user_id: int) -> User | None:
        return self.db.scalar(select(User).where(User.id == user_id))
