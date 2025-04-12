from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from src.models import Base


class Secrets(Base):
    __tablename__ = "secret"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(128), nullable=False, unique=True)
    secret_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    available = Column(Boolean, default=True)
    passphrase_hash = Column(String(256))
    
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="secrets")
    
    def __repr__(self):
        return f"<Secret(id={self.id}, hash={self.secret_hash})>"