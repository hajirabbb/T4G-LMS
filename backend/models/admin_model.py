from sqlalchemy import Column, String
from sqlalchemy.dialects.sqlite import TEXT
from database import Base
import uuid


class Admin(Base):
    __tablename__ = "admins"

    id = Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
