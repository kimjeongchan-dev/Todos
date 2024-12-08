from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo, User
from database.repository import TodoRepository, UserRepository
from schema.request import CreateTodoRequest, UpdateTodoRequest
from schema.response import GetTodosResponse, TodoSchema
from security import get_access_token
from service.user import UserService


router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", status_code=200)
def get_todos_handler(
    order: str | None = None, 
    user_repository: UserRepository = Depends(UserRepository),
    user_service: UserService = Depends(UserService),
    access_token: str = Depends(get_access_token)
) -> GetTodosResponse:
    
    user_id: int = user_service.decode_token(token=access_token)
    user: User | None = user_repository.get_user_by_user_id(user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    todos: list[Todo] = user.todos
    if order == "DESC":
        return GetTodosResponse(todos=[TodoSchema.from_orm(todo) for todo in todos[::-1]])

    return GetTodosResponse(todos=[TodoSchema.from_orm(todo) for todo in todos])


@router.get("/{todo_id}", status_code=200)
def get_todo_by_todo_id_handler(todo_id: int, todo_repository: TodoRepository = Depends(TodoRepository)) -> TodoSchema:
    todo: Todo | None = todo_repository.get_todo_by_todo_id(todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return TodoSchema.from_orm(todo)


@router.post("/", status_code=201)
def create_todo_handler(request: CreateTodoRequest, todo_repository: TodoRepository = Depends(TodoRepository)) -> TodoSchema:
    todo: Todo = todo_repository.create_todo(request=request)
    return TodoSchema.from_orm(todo)


@router.patch("/{todo_id}", status_code=200)
def update_todo_handler(todo_id: int, request: UpdateTodoRequest, todo_repository: TodoRepository = Depends(TodoRepository)) -> TodoSchema:
    todo: Todo | None = todo_repository.get_todo_by_todo_id(todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated_todo: Todo = todo_repository.update_todo(todo=todo, request=request)
    return TodoSchema.from_orm(updated_todo)


@router.delete("/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int, todo_repository: TodoRepository = Depends(TodoRepository)) -> None:
    todo: Todo | None = todo_repository.get_todo_by_todo_id(todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_repository.delete_todo(todo=todo)
