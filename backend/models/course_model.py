from sqlalchemy import Column, String, Enum, Text
from sqlalchemy.dialects.sqlite import TEXT
from database import Base
import enum
import uuid


class StatusEnum(str, enum.Enum):
    active = "Active"
    inactive = "Inactive"


class Course(Base):
    __tablename__ = "courses"

    id = Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    track = Column(String(50), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.active)
