from pydantic import BaseModel, EmailStr
from enum import Enum


class TrackEnum(str, Enum):
    frontend = "Frontend"
    backend = "Backend"


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    track: TrackEnum


class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class StudentResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    student_id: str
    track: TrackEnum
    
    
    class Config:
        from_attributes = True


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
