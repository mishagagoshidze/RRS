import bcrypt
from datetime import datetime, timedelta, timezone
#from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Optional
from sqlalchemy.orm import Session

from app.db.models import Users

# ==============================
# Password hashing setup
# ==============================

'''
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=True
)
'''

# ==============================
# JWT Config
# ==============================

SECRET_KEY = "kutaisi_cue_rrs_secret"   # რეალური secret-ით
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ==============================
# Password functions
# ==============================

def hash_password(password: str) -> str:
    """პაროლის დაჰეშირება პირდაპირ bcrypt ბიბლიოთეკით"""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """პაროლის შემოწმება"""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

# ==============================
# Token creation
# ==============================

def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT ტოკენის გენერაცია"""

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode a JWT token and return its payload."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def get_current_user(token: str, db: Session) -> Optional[Users]:
    """Return the current authenticated user from a JWT token."""
    payload = decode_token(token)
    if not payload:
        return None

    email = payload.get("sub")
    if not email:
        return None

    return db.query(Users).filter(Users.email == email).first()