from pydantic import EmailStr
from sqlalchemy import select
from models.users import UsersOrm
from repositories.base import BaseRepository
from schemas.users import User, UserWithHashedPass

class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model =  result.scalars().one()
        return UserWithHashedPass.model_validate(model)
            