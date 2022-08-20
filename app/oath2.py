from datetime import datetime, timedelta
from jose import JWTError, jwt
from .config import settings

# SECRET_KEY
#ALGORITHM
#Expiration time of token

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.token_expiration_time_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt  = jwt.encode(to_encode, settings.token_secret_key, algorithm=settings.token_algorithm)
    return encoded_jwt