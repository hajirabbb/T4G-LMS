from sqlalchemy.orm import Session
from models.enrollment_model import Enrollment
from schemas.enrollment_schema import EnrollmentCreate


def get_enrollments_by_course(db: Session, course_id: str):
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()


def get_enrollments_by_student(db: Session, student_id: str):
    return db.query(Enrollment).filter(Enrollment.student_id == student_id).all()


def enroll_student(db: Session, enrollment: EnrollmentCreate):
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        return None
    db_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def unenroll_student(db: Session, student_id: str, course_id: str):
    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id
    ).first()
    if enrollment:
        db.delete(enrollment)
        db.commit()
    return enrollment
