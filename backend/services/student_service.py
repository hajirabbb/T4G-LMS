from sqlalchemy.orm import Session
from sqlalchemy import or_
from auth import hash_password
from models.student_model import Student
from schemas.student_schema import StudentCreate
import uuid


def create_student(db: Session, student: StudentCreate):
    db_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        student_id=generate_student_id(),
        track=student.track,
        password=hash_password("temp1234")
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student



def get_all_students(db: Session):
    return db.query(Student).all()


def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


 

def search_students(db: Session, q: str):
    keyword = f"%{q.strip()}%"
    return (
        db.query(Student)
        .filter(
            or_(
                Student.first_name.ilike(keyword),
                Student.last_name.ilike(keyword),
                Student.email.ilike(keyword),
                Student.student_id.ilike(keyword),
                Student.track.ilike(keyword),
            )
        )
        .all()
    )





def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
    return student


def generate_student_id():
    unique = uuid.uuid4().hex[:6].upper()
    return f"TG-2026-{unique}"


