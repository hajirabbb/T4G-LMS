from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.student_model import Student
from services.student_service import (
    get_all_students,
    get_student_by_id,
    create_student,
    delete_student
)
from schemas.student_schema import StudentCreate, StudentResponse, StudentLogin
from auth import verify_password, create_access_token

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=list[StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return get_all_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: str, db: Session = Depends(get_db)):
    student = get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=StudentResponse)
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db, student)


@router.delete("/{student_id}")
def remove_student(student_id: str, db: Session = Depends(get_db)):
    student = delete_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


@router.post("/login")
def login_student(student: StudentLogin, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(
        Student.email == student.email).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not verify_password(student.password, db_student.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = create_access_token(
        data={"sub": db_student.email, "role": "student"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "student": {
            "id": db_student.id,
            "first_name": db_student.first_name,
            "last_name": db_student.last_name,
            "email": db_student.email,
            "student_id": db_student.student_id,
            "track": db_student.track
        }
    }
