from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    contents: str
    is_done: bool = False

class UpdateTodoRequest(BaseModel):
    contents: str
    is_done: bool

class SignUpRequest(BaseModel):
    name: str
    password: str


class LoginRequest(BaseModel):
    name: str
    password: str


class CreateOptRequest(BaseModel):
    email: str


class VerifyOptRequest(BaseModel):
    email: str
    opt: int
