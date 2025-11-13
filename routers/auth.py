from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from auth.jwt import hash_password, verify_password, create_token
from schemas.user import UserCreate, Token

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/register", response_model=None)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if data.password != data.password2:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already used")
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
    )
    db.add(user)
    db.commit()
    return {"message": "created"}


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(400, "Неверно")
    return {"access_token": create_token({"email": user.email}), "token_type": "bearer"}
