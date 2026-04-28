import bcrypt
from datetime import datetime, timedelta, timezone
#from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Optional

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