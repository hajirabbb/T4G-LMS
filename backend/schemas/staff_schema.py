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

    class Config:
        from_attributes = True


class StaffLogin(BaseModel):
    email: EmailStr
    password: str
