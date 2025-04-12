from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.models import Base


class Logs(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True)
    action = Column(String(120), nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)
    ip = Column(String(100), nullable=False)