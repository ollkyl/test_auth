from datetime import datetime, timedelta
from jwt import encode
from bcrypt import hashpw, gensalt, checkpw
from dotenv import load_dotenv
import os
from typing import Any

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set in environment (.env)")


def hash_password(password: str) -> str:
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_token(data: dict[str, Any], expires_hours: int = 1) -> str:
    expire = datetime.utcnow() + timedelta(hours=expires_hours)
    payload = {**data, "exp": expire}
    return encode(payload, SECRET_KEY, algorithm=ALGORITHM)
