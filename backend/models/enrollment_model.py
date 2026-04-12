from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.sqlite import TEXT
from database import Base
import uuid
from datetime import datetime


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(TEXT, ForeignKey("students.id"), nullable=False)
    course_id = Column(TEXT, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
