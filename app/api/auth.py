from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.models.user import User
from app.security import create_access_token, hash_password, verify_password
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str
class LoginRequest(BaseModel):
    username: str
    password: str
@router.post("/register")
def register_user(data: RegisterRequest):
    db = SessionLocal()
    try:
        existing_user = (
            db.query(User)
            .filter(User.username == data.username)
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )
        user = User(
            username=data.username,
            password_hash=hash_password(data.password),
            role=data.role.upper(),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return {
            "success": True,
            "message": "User registered successfully",
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        }
    finally:
        db.close()
@router.post("/login")
def login_user(data: LoginRequest):
    db = SessionLocal()
    try:
        user = (
            db.query(User)
            .filter(User.username == data.username)
            .first()
        )
        if not user or not verify_password(
            data.password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="User account is inactive"
            )
        access_token = create_access_token(
            {
                "sub": str(user.id),
                "username": user.username,
                "role": user.role
            }
        )
        return {
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        }
    finally:
        db.close()