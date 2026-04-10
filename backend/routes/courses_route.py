from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.course_service import (
    get_all_courses,
    get_course_by_id,
    create_course,
    update_course,
    delete_course
)
from schemas.course_schema import CourseCreate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=list[CourseResponse])
def read_courses(db: Session = Depends(get_db)):
    return get_all_courses(db)


@router.get("/{course_id}", response_model=CourseResponse)
def read_course(course_id: str, db: Session = Depends(get_db)):
    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/", response_model=CourseResponse)
def add_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db, course)


@router.put("/{course_id}", response_model=CourseResponse)
def edit_course(course_id: str, course: CourseCreate, db: Session = Depends(get_db)):
    updated = update_course(db, course_id, course)
    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated


@router.delete("/{course_id}")
def remove_course(course_id: str, db: Session = Depends(get_db)):
    course = delete_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}
