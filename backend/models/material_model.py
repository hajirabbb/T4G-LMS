from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.sqlite import TEXT
from database import Base
import uuid
from datetime import datetime


class Material(Base):
    __tablename__ = "materials"

    id = Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(TEXT, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    file_name = Column(String(200), nullable=False)
    file_data = Column(TEXT, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
