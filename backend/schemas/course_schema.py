from pydantic import BaseModel
from enum import Enum


class StatusEnum(str, Enum):
    active = "Active"
    inactive = "Inactive"


class CourseCreate(BaseModel):
    course_name: str
    description: str | None = None
    track: str
    status: StatusEnum = StatusEnum.active


class CourseResponse(BaseModel):
    id: str
    course_name: str
    description: str | None = None
    track: str
    status: StatusEnum

    class Config:
        from_attributes = True
