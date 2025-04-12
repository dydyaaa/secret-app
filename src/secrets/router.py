from fastapi import APIRouter, Depends, HTTPException, Query, Request
from src.secrets.service import SecretServ
from src.config import settings
from src.database import get_db
from src.dependencies import get_redis
from src.secrets.schemas import SecretCreate, SecretBase, SecretResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.utils import get_current_user
from src.auth.models import User
from typing import Optional
from redis.asyncio import Redis


router = APIRouter()


@router.post('/', response_model=SecretBase)
async def create_secret(request: Request,
                        secret_create: SecretCreate, 
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_user),
                        redis: Redis = Depends(get_redis)
                        ):
    
    ip_address = request.client.host
    unique_key = await SecretServ.create_secret(db, secret_create, user, redis, ip_address)

    return SecretBase(
        unique_key=unique_key
    )
    
@router.get('/{unique_key}', response_model=SecretResponse)
async def get_secret(request: Request,
                     unique_key: str,
                     passphrase: Optional[str] = Query(''),
                     db: AsyncSession = Depends(get_db),
                     user: User = Depends(get_current_user),
                     redis: Redis = Depends(get_redis)
                     ):
    
    ip_address = request.client.host
    secret = await SecretServ.get_secret(db, unique_key, passphrase, user, redis, ip_address)
    
    return SecretResponse(
        secret=secret
    )
    
@router.delete('/{unique_key}')
async def delete_secret(request: Request,
                        unique_key: str,
                        passphrase: Optional[str] = Query(''),
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_user),
                        redis: Redis = Depends(get_redis)
                        ):
    
    ip_address = request.client.host
    result = await SecretServ.delete_secret(db, unique_key, passphrase, user, redis, ip_address)
    
    return {"status": f"{result}"}