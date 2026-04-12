from pydantic import BaseModel
from datetime import datetime


class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: str


class EnrollmentResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    enrolled_at: datetime

    class Config:
        from_attributes = True
