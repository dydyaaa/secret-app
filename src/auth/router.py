from fastapi import APIRouter, Depends, HTTPException
from src.auth.service import AuthService
from src.config import settings
from src.database import get_db
from src.auth.schemas import UserBase, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

    
@router.post('/register', response_model=UserBase)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    user, jwt_token = await AuthService.register(db, user_create)

    return UserBase(
        id=user.id,
        email=user.email,
        name=user.name,
        jwt_code=jwt_token
    )