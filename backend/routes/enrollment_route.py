from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.enrollment_service import (
    get_enrollments_by_course,
    get_enrollments_by_student,
    enroll_student,
    unenroll_student
)
from schemas.enrollment_schema import EnrollmentCreate, EnrollmentResponse

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("/", response_model=EnrollmentResponse)
def enroll(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    result = enroll_student(db, enrollment)
    if not result:
        raise HTTPException(
            status_code=400, detail="Student already enrolled in this course")
    return result


@router.get("/course/{course_id}")
def get_course_enrollments(course_id: str, db: Session = Depends(get_db)):
    enrollments = get_enrollments_by_course(db, course_id)
    return {"course_id": course_id, "enrolled_students": len(enrollments)}


@router.get("/student/{student_id}")
def get_student_enrollments(student_id: str, db: Session = Depends(get_db)):
    return get_enrollments_by_student(db, student_id)


@router.delete("/")
def unenroll(student_id: str, course_id: str, db: Session = Depends(get_db)):
    result = unenroll_student(db, student_id, course_id)
    if not result:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"message": "Student unenrolled successfully"}
