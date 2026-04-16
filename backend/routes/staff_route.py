from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.staff_model import Staff
from services.staff_service import (
    get_all_staff,
    get_staff_by_id,
    create_staff,
    delete_staff,
    get_staff_by_email,
    search_staff
)
from schemas.staff_schema import StaffCreate, StaffResponse, StaffLogin, ChangePassword, ForgotPassword, ResetPassword

from auth import verify_password, create_access_token, hash_password, get_current_user

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.get("/", response_model=list[StaffResponse])
def read_staff(db: Session = Depends(get_db)):
    return get_all_staff(db)


@router.get("/search")
def search_staff_route(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    results = search_staff(db, q)
    return results


@router.delete("/{staff_id}")
def remove_staff(staff_id: str, db: Session = Depends(get_db)):
    staff = delete_staff(db, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"message": "Staff deleted successfully"}



@router.get("/{staff_id}", response_model=StaffResponse)
def read_staff_member(staff_id: str, db: Session = Depends(get_db)):
    staff = get_staff_by_id(db, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff


@router.post("/", response_model=StaffResponse)
def add_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    existing = get_staff_by_email(db, staff.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    return create_staff(db, staff)


@router.post("/login")
def login_staff(staff: StaffLogin, db: Session = Depends(get_db)):
    db_staff = get_staff_by_email(db, staff.email)
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    if not verify_password(staff.password, db_staff.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = create_access_token(data={"sub": db_staff.email, "role": "staff"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "staff": {
            "id": db_staff.id,
            "first_name": db_staff.first_name,
            "last_name": db_staff.last_name,
            "email": db_staff.email,
            "track": db_staff.track,
            "is_default_password": db_staff.is_default_password
        }
    }




@router.put("/change-password")
def change_staff_password(
    passwords: ChangePassword,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    staff = db.query(Staff).filter(Staff.email == current_user).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    if not verify_password(passwords.current_password, staff.password):
        raise HTTPException(
            status_code=401, detail="Current password is incorrect")
    staff.password = hash_password(passwords.new_password)
    staff.is_default_password = False
    db.commit()
    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
def staff_forgot_password(data: ForgotPassword, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.email == data.email).first()
    if not staff:
        raise HTTPException(
            status_code=404, detail="No account found with this email")
    return {"message": "Email found", "email": data.email}


@router.post("/reset-password")
def staff_reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.email == data.email).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    staff.password = hash_password(data.new_password)
    staff.is_default_password = False
    db.commit()
    return {"message": "Password reset successfully"}
