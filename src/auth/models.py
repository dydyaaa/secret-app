from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    name = Column(String(120), nullable=False)
    password_hash = Column(String(256), nullable=False)
    
    secrets = relationship("Secrets", back_populates="user", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"