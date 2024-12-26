from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    nickname: str
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    nickname: str
    hashed_password: str

class User(BaseModel):
    id: int
    email: EmailStr
    
    
    model_config = ConfigDict(from_attributes=True)