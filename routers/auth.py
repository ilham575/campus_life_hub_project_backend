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
    get_current_user, get_current_active_user, require_admin, get_or_create_roles
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
    )
    roles = user.roles if user.roles else ["user"]
    db_user.roles = get_or_create_roles(db, roles)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        name=db_user.name,
        student_id=db_user.student_id,
        faculty=db_user.faculty,
        year=db_user.year,
        created_at=db_user.created_at,
        roles=[role.name for role in db_user.roles]
    )

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
        "user": UserResponse(
            id=user.id,
            username=user.username,
            name=user.name,
            student_id=user.student_id,
            faculty=user.faculty,
            year=user.year,
            created_at=user.created_at, 
            roles=[role.name for role in user.roles]
        )
    }

# ------------------------
# Me
# ------------------------
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        name=current_user.name,
        student_id=current_user.student_id,
        faculty=current_user.faculty,
        year=current_user.year,
        created_at=current_user.created_at,
        roles=[role.name for role in current_user.roles]
    )

@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(user_id: int,
                     role_update: RoleUpdate,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.roles = get_or_create_roles(db, role_update.roles)
    db.commit()
    db.refresh(user)
    return UserResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        student_id=user.student_id,
        faculty=user.faculty,
        year=user.year,
        created_at=user.created_at, 
        roles=[role.name for role in user.roles]
    )

# ------------------------
# Admin-only
# ------------------------
@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    users = db.query(User).all()
    return [
        UserResponse(
            id=u.id,
            username=u.username,
            name=u.name,
            student_id=u.student_id,
            faculty=u.faculty,
            year=u.year,
            created_at=u.created_at,
            roles=[role.name for role in u.roles]
        ) for u in users
    ]

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        student_id=user.student_id,
        faculty=user.faculty,
        year=user.year,
        created_at=user.created_at,
        roles=[role.name for role in user.roles]
    )