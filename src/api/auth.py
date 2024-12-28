from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Request, Response

from config import settings
from services.auth import AuthService
from src.repositories.user import UsersRepository
from src.database import async_session_maker
import jwt

from passlib.context import CryptContext

from schemas.users import UserAdd, UserRequestAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm= settings.JWT_ALGORITHM)
    return encoded_jwt


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
):
    # hashed_password = pwd_context.hash(data.password)
    # new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, nickname=data.nickname)
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=data.email)
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, nickname=data.nickname)
    async with async_session_maker() as session: 
       await UsersRepository(session).add(new_user_data)
       await session.commit()
    
    return {"status": "OK"}

@router.get("/only_auth")
async def only_auth(
    request: Request,
):
    cookies = request.cookies
    access_token = cookies.get("access token") or None
    if not access_token:
        raise HTTPException(status_code=401, detail="Не аутенфецирован")
    return {"message": "Access granted", "access_token": access_token}