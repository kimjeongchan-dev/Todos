from fastapi import APIRouter, Depends, HTTPException

from database.orm import User
from schema.request import LoginRequest, SignUpRequest
from schema.response import JWTResponse, SignUpResponse
from database.repository import UserRepository
from service.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/sign-up", status_code=201)
def sign_up_handler(
    request: SignUpRequest, 
    user_service: UserService = Depends(UserService), 
    user_repository: UserRepository = Depends(UserRepository)
) -> SignUpResponse:
    hashed_password: str = user_service.hash_password(password=request.password)
    new_user: User = user_repository.create_user(name=request.name, password=hashed_password)
    return SignUpResponse.from_orm(new_user)


@router.post("/login", status_code=200)
def login_handler(
    request: LoginRequest, 
    user_service: UserService = Depends(UserService), 
    user_repository: UserRepository = Depends(UserRepository)
) -> JWTResponse:
    user: User = user_repository.get_user_by_name(name=request.name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user_service.verify_password(password=request.password, hashed_password=user.password):
        raise HTTPException(status_code=401, detail="Not authorized")
    
    access_token: str = user_service.create_token(user_id=user.id)
    return JWTResponse(access_token=access_token)
