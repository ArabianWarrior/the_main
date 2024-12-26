from models.users import UsersOrm
from repositories.base import BaseRepository
from schemas.users import User

class UserRepository(BaseRepository):
    model = UsersOrm
    schema = User