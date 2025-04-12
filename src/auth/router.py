from fastapi import APIRouter, Depends, HTTPException
from src.auth.service import AuthService
from src.config import settings
from src.database import get_db
from src.auth.schemas import UserBase, UserCreate, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.utils import get_current_user
from src.auth.models import User


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
    
@router.post('/login', response_model=UserBase)
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    user, jwt_token = await AuthService.login(db, user_login)
    
    return UserBase(
        id=user.id,
        email=user.email,
        name=user.name,
        jwt_code=jwt_token
    )
    