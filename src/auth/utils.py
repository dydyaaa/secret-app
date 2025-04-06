from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from src.config import settings
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from sqlalchemy.future import select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.database import get_db


security = HTTPBearer()

def create_access_token(user_id: str) -> str:
    expires = datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRES)
    to_encode = {"sub": user_id, "exp": expires}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный токен",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            user_id = int(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный токен: 'sub' должен быть числом",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user