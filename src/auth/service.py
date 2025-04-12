import logging
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.config import settings
from src.auth.models import User
from src.auth.utils import create_access_token
from fastapi import HTTPException, status
from src.auth.schemas import UserCreate, UserLogin


logger = logging.getLogger("app.auth")

class AuthService:
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    @classmethod
    async def register(cls, db: AsyncSession, user_data: UserCreate) -> User:
        """
        """
        result = await db.execute(select(User).filter_by(email=user_data.email))
        existing_user = result.scalars().first()

        if existing_user:
            logger.info(f'Пользователь уже существует: {existing_user.email}')
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail="Пользоваель с таким логином уже зарегистрирован!"
            )
        
        password_hash = cls.pwd_context.hash(user_data.password)

        new_user = User(email=user_data.email, name=user_data.name, password_hash=password_hash)
        jwt_token = create_access_token(str(new_user.id))
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user, jwt_token
    
    @classmethod
    async def login(cls, db: AsyncSession, user_data: UserLogin):
        """
        """
        result = await db.execute(select(User).filter_by(email=user_data.email))
        existing_user = result.scalars().first()

        if not existing_user:
            logger.info(f'Пользователь с таким email не существует существует: {existing_user.email}')
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail="Пользоваель с таким email еще не зарегистрирован!"
            )
            
        if not cls.pwd_context.verify(user_data.password, existing_user.password_hash):
            logger.info(f'Неправильный пароль для пользователя {existing_user.email}')
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail='Неверный пароль!'
            )
            
        jwt_token = create_access_token(str(existing_user.id))
            
        return existing_user, jwt_token