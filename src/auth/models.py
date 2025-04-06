from sqlalchemy import Column, Integer, String, Boolean
from src.models import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    name = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"