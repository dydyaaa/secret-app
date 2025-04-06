from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserBase(BaseModel):
    id: int
    email: EmailStr
    name: str
    jwt_code: str

    class Config:
        orm_mode = True