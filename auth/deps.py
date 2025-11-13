from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode
from database import get_db
from models.user import User
from auth.jwt import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if not email:
            raise HTTPException(401)
    except:
        raise HTTPException(401, "Invalid token")

    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    if not user:
        raise HTTPException(401)
    return user
