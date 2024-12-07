from pydantic import BaseModel


class TodoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    @classmethod
    def from_orm(cls, obj):
        return cls(**obj.__dict__)


class GetTodosResponse(BaseModel):
    todos: list[TodoSchema]
