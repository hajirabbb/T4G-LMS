from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.admin_model import Admin
from auth import hash_password, verify_password, create_access_token
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/admin", tags=["Admin"])


class AdminCreate(BaseModel):
    email: EmailStr
    password: str


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    existing = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    new_admin = Admin(
        email=admin.email,
        password=hash_password(admin.password)
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message": "Admin registered successfully"}


@router.post("/login")
def login_admin(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    if not verify_password(admin.password, db_admin.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = create_access_token(data={"sub": db_admin.email})
    return {"access_token": token, "token_type": "bearer"}

