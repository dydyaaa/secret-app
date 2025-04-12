from sqlalchemy.ext.asyncio import AsyncSession
from src.logs.models import Logs


class LogsServ:
    
    @staticmethod
    async def write_log(db: AsyncSession, log: str, ip: str):
        
        new_log = Logs(
            action=log,
            ip=ip
        )
        
        db.add(new_log)
        
        await db.commit()
        await db.refresh(new_log)