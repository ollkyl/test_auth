from datetime import datetime, timedelta
from jwt import encode
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(p):
    return pwd_context.hash(p)


def verify_password(p, h):
    return pwd_context.verify(p, h)


def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=1)
    return encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
