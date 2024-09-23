from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from core.config import settings


crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = "/token")

ALGORITHM = "HS256"


def hash_password(password):
    return crypt_context.hash(password)
    

def authenticate(password, hashed_password):
    if crypt_context.verify(password, hashed_password):
        return True
    
    
def create_access_token(user_id: int, expire_minutes: int | None = None) -> str:
    if not user_id:
        raise ValueError("User ID is required")
    
    payload = {"id": user_id}
    if expire_minutes:
        payload["exp"] = datetime.utcnow() + timedelta(minutes=expire_minutes)
    else:
        payload["exp"] = datetime.utcnow() + timedelta(minutes=settings.EXPIRE_MINUTES)
    
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)