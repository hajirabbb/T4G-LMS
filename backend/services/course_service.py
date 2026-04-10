from sqlalchemy.orm import Session
from models.course_model import Course
from schemas.course_schema import CourseCreate


def get_all_courses(db: Session):
    return db.query(Course).all()


def get_course_by_id(db: Session, course_id: str):
    return db.query(Course).filter(Course.id == course_id).first()


def create_course(db: Session, course: CourseCreate):
    db_course = Course(
        course_name=course.course_name,
        description=course.description,
        track=course.track,
        status=course.status
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: int, course: CourseCreate):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db_course.course_name = course.course_name
        db_course.description = course.description
        db_course.track = course.track
        db_course.status = course.status
        db.commit()
        db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
    return db_course
