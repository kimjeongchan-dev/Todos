from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from database.orm import User
from schema.request import CreateOptRequest, LoginRequest, SignUpRequest, VerifyOptRequest
from schema.response import JWTResponse, SignUpResponse, UserResponse
from database.repository import UserRepository
from security import get_access_token
from service.user import UserService
from cache import redis_client
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


@router.post("/email/otp", status_code=200)
def create_opt_handler(
    request: CreateOptRequest, 
    user_service: UserService = Depends(UserService), 
    _: str = Depends(get_access_token)
) -> dict:
    opt: int = user_service.create_opt()
    redis_client.set(name=request.email, value=opt, ex=60)
    return {"opt": opt}


@router.post("/email/otp/verify", status_code=200)
def verify_opt_handler(
    request: VerifyOptRequest, 
    background_tasks: BackgroundTasks,
    user_service: UserService = Depends(UserService), 
    user_repository: UserRepository = Depends(UserRepository),
    access_token: str = Depends(get_access_token)
) -> None:
    otp: str | None = redis_client.get(name=request.email)
    if otp is None:
        raise HTTPException(status_code=400, detail="Bad request")
    
    if request.opt != int(otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    user_id: int = user_service.decode_token(token=access_token)
    user: User | None = user_repository.get_user_by_user_id(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    background_tasks.add_task(user_service.send_email_to_user, email=request.email)
    return UserResponse.from_orm(user)
