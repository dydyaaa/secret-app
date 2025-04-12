import logging
import uuid
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.config import settings
from src.secrets.models import Secrets
from src.secrets.utils import encrypt_string, decrypt_string
from src.auth.utils import get_current_user
from fastapi import HTTPException, status
from src.secrets.schemas import SecretCreate, SecretBase
from redis.asyncio import Redis
from src.logs.service import LogsServ
import json


logger = logging.getLogger("app.secrets")

class SecretServ:
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    @classmethod
    async def create_secret(cls, db: AsyncSession, secret_data: SecretCreate, user, redis: Redis, ip):
        
        unique_key = str(uuid.uuid4())
        secret_hash = encrypt_string(secret_data.secret)
        
        if not secret_data.passphrase:
            passphrase_hash = cls.pwd_context.hash('')
        else:
            passphrase_hash = cls.pwd_context.hash(secret_data.passphrase)
        
        expires_at = None if secret_data.ttl_seconds == 0 else datetime.utcnow() + timedelta(seconds=secret_data.ttl_seconds)

        new_secret = Secrets(
            uuid=unique_key,
            secret_hash=secret_hash,
            expires_at=expires_at,
            user_id=user.id,
            passphrase_hash=passphrase_hash
        )
        
        db.add(new_secret)
        await db.commit()
        await db.refresh(new_secret)
        
        try:
            data_to_redis = {
                "secret_hash": secret_hash,
                "passphrase_hash": passphrase_hash,
                "user_id": int(user.id)
            }
            if secret_data.ttl_seconds == 0:
                ttl = 60 * 5
            else:
                ttl = secret_data.ttl_seconds
            await redis.setex(unique_key, ttl, json.dumps(data_to_redis))
        except Exception as e:
            logger.error(f'{e}')
        
        await LogsServ.write_log(db, f'Создан секрет для {user.email}', ip)
        return unique_key

    @classmethod
    async def get_secret(cls, db: AsyncSession, unique_key: str, passphrase: str, user, redis: Redis, ip):
        
        
        result = await redis.get(unique_key)
        if result:
            data = json.loads(result)
            if not cls.pwd_context.verify(passphrase, data.get('passphrase_hash')):
                return 'Неверная кодовая фраза'
            
            if not data.get('user_id') == user.id:
                return 'Секрет не найден!'
            
            await redis.delete(unique_key)
            
            secret_hash = data.get('secret_hash')
        
        else:
            
            result = await db.execute(select(Secrets).filter_by(
                                                                uuid=unique_key,
                                                                user_id=user.id,
                                                                available=True))
            
            existing_secret = result.scalars().first()
            if not existing_secret:
                return 'Секрет не найден!'
            
            if not cls.pwd_context.verify(passphrase, existing_secret.passphrase_hash):
                return 'Неверная кодовая фраза'
            
            secret_hash = existing_secret.secret_hash
        
        await db.execute(update(Secrets).filter_by(
                                            uuid=unique_key, 
                                            user_id=user.id, 
                                            available=True
                                            ).values(available=False))
        await db.commit()
            
        secret = decrypt_string(secret_hash)
        
        await LogsServ.write_log(db, f'Чтение секрета для {user.email}', ip)
        return secret
    
    @classmethod
    async def delete_secret(cls, db: AsyncSession, unique_key: str, passphrase: str, user, redis: Redis, ip):
        
        await redis.delete(unique_key)
        
        result = await db.execute(select(Secrets).filter_by(
                                                uuid=unique_key,
                                                user_id=user.id))
        
        existing_secret = result.scalars().first()
        
        if not existing_secret:
            return 'Секрет не найден'
        
        if existing_secret.passphrase_hash:
            if not cls.pwd_context.verify(passphrase, existing_secret.passphrase_hash):
                return 'Неверная кодовая фраза'
        
        await db.execute(delete(Secrets).filter_by(
                                        uuid=unique_key,
                                        user_id=user.id))
        await db.commit()
        
        await LogsServ.write_log(db, f'Удаление секрета для {user.email}', ip)
        return 'Секрет удален'