from pydantic import BaseModel, EmailStr
from enum import Enum


class StaffTrackEnum(str, Enum):
    frontend = "Frontend"
    backend = "Backend"


class StaffCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    track: StaffTrackEnum


class StaffResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    staff_id: str
    track: StaffTrackEnum
    
    
class StaffLogin(BaseModel):
    email: EmailStr
    password: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str

    class Config:
        from_attributes = True


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str
