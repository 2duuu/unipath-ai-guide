"""Authentication endpoints: register, login, current user."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user_id,
    hash_password,
    verify_password,
)
from app.db.database import SessionLocal, StudentProfileDB

router = APIRouter()


@router.post("/api/auth/register", response_model=TokenResponse)
async def register(request: RegisterRequest):
    """Register a new user."""
    db = SessionLocal()
    try:
        # Check if username already exists
        existing_user = db.query(StudentProfileDB).filter(
            StudentProfileDB.username == request.username
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Check if email already exists
        existing_email = db.query(StudentProfileDB).filter(
            StudentProfileDB.email == request.email
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_pwd = hash_password(request.password)
        new_user = StudentProfileDB(
            username=request.username,
            email=request.email,
            password_hash=hashed_pwd,
            name=request.name or request.username,
            is_verified=False,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create tokens
        access_token = create_access_token(data={"user_id": new_user.id})
        refresh_token = create_refresh_token(data={"user_id": new_user.id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "name": new_user.name,
                "is_verified": new_user.is_verified
            }
        }
    finally:
        db.close()


@router.post("/api/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login with username or email and password."""
    db = SessionLocal()
    try:
        # Find user by username or email
        user = db.query(StudentProfileDB).filter(
            (StudentProfileDB.username == request.username) | 
            (StudentProfileDB.email == request.username)
        ).first()
        
        if not user or not user.password_hash:
            raise HTTPException(
                status_code=401, 
                detail="Incorrect username/email or password"
            )
        
        # Verify password
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=401, 
                detail="Incorrect username/email or password"
            )
        
        # Update last login
        user.last_login = datetime.utcnow().isoformat()
        db.commit()
        
        # Create tokens
        access_token = create_access_token(data={"user_id": user.id})
        refresh_token = create_refresh_token(data={"user_id": user.id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "is_verified": user.is_verified
            }
        }
    finally:
        db.close()


@router.get("/api/auth/me", response_model=UserResponse)
async def get_current_user(user_id: int = Depends(get_current_user_id)):
    """Get current authenticated user's profile."""
    db = SessionLocal()
    try:
        user = db.query(StudentProfileDB).filter(StudentProfileDB.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "is_verified": user.is_verified,
            "created_at": user.created_at
        }
    finally:
        db.close()
