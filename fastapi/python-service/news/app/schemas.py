from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    keyword: str

class User(BaseModel):
    id: int
    email: EmailStr
    keyword: str

    class Config:
        orm_mode = True
