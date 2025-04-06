import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.config import settings
from src.auth.models import User
from src.auth.utils import create_access_token
from fastapi import HTTPException, status
from src.auth.schemas import UserCreate


logger = logging.getLogger("app.auth")

class AuthService:
    @staticmethod
    async def register(db: AsyncSession, user_data: UserCreate) -> User:
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

        new_user = User(email=user_data.email, name=user_data.name)
        jwt_token = create_access_token(str(new_user.id))
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user, jwt_token
        