from sqlalchemy.orm import Session
from models.staff_model import Staff
from schemas.staff_schema import StaffCreate
from auth import hash_password
import uuid


def generate_staff_id():
    unique = uuid.uuid4().hex[:6].upper()
    return f"STF-2026-{unique}"


def get_all_staff(db: Session):
    return db.query(Staff).all()


def get_staff_by_id(db: Session, staff_id: str):
    return db.query(Staff).filter(Staff.id == staff_id).first()


def get_staff_by_email(db: Session, email: str):
    return db.query(Staff).filter(Staff.email == email).first()


def create_staff(db: Session, staff: StaffCreate):
    db_staff = Staff(
        first_name=staff.first_name,
        last_name=staff.last_name,
        email=staff.email,
        staff_id=generate_staff_id(),
        track=staff.track,
        password=hash_password("temp1234")
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff


def search_staff(db: Session, q: str):
    """
    Search staff by first name, last name, email, staff ID, or track.
    Case-insensitive, partial match.
    """
    keyword = f"%{q.strip()}%"
    return (
        db.query(Staff)
        .filter(
            or_(
                Staff.first_name.ilike(keyword),
                Staff.last_name.ilike(keyword),
                Staff.email.ilike(keyword),
                Staff.staff_id.ilike(keyword),
                Staff.track.ilike(keyword),
            )
        )
        .all()
    )


def delete_staff(db: Session, staff_id: str):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if staff:
        db.delete(staff)
        db.commit()
    return staff
