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


class SignUpResponse(BaseModel):
    id: int
    name: str

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name
        )


class JWTResponse(BaseModel):
    access_token: str



class UserResponse(BaseModel):
    id: int
    name: str

    @classmethod
    def from_orm(cls, obj):
        return cls(id=obj.id, name=obj.name)
