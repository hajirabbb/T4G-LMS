from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.sqlite import TEXT
from database import Base
import enum
import uuid


class StaffTrackEnum(str, enum.Enum):
    frontend = "Frontend"
    backend = "Backend"


class Staff(Base):
    __tablename__ = "staff"

    id = Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    staff_id = Column(String(20), unique=True, nullable=False)
    track = Column(Enum(StaffTrackEnum), nullable=False)
    password = Column(String(255), nullable=False)
