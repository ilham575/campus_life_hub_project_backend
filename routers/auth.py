# routers/auth.py

from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.auth import UserCreate, UserResponse, UserUpdate, Token, TokenData, RoleUpdate
from services.auth_service import (
    authenticate_user, create_access_token, get_password_hash,
    get_current_user, get_current_active_user, require_admin
)

router = APIRouter()

# ------------------------
# Register
# ------------------------
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if user.student_id and db.query(User).filter(User.student_id == user.student_id).first():
        raise HTTPException(status_code=400, detail="Student ID already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        name=user.name,
        student_id=user.student_id,
        faculty=user.faculty,
        year=user.year,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ------------------------
# Login
# ------------------------
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }

# ------------------------
# Me
# ------------------------
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_profile(user_update: UserUpdate,
                        current_user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    if user_update.name is not None:
        current_user.name = user_update.name
    if user_update.student_id is not None:
        existing = db.query(User).filter(User.student_id == user_update.student_id,
                                         User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Student ID already exists")
        current_user.student_id = user_update.student_id
    if user_update.faculty is not None:
        current_user.faculty = user_update.faculty
    if user_update.year is not None:
        current_user.year = user_update.year

    db.commit()
    db.refresh(current_user)
    return current_user

# ------------------------
# Admin-only
# ------------------------
@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    return db.query(User).all()

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(user_id: int,
                     role_update: RoleUpdate,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return user
