from fastapi import APIRouter

from src.repositories.user import UserRepository
from src.database import async_session_maker

from passlib.context import CryptContext

from schemas.users import UserAdd, UserRequestAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, nickname=data.nickname)
    async with async_session_maker() as session: 
       await UserRepository(session).add(new_user_data)
       await session.commit()
    
    return {"status": "OK"}
