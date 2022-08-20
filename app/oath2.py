from datetime import datetime, timedelta
from jose import JWTError, jwt
from .config import settings
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import  OAuth2PasswordBearer

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
#ALGORITHM
#Expiration time of token

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.token_expiration_time_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt  = jwt.encode(to_encode, settings.token_secret_key, algorithm=settings.token_algorithm)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        
        payload=jwt.decode(token, settings.token_secret_key, algorithms=[settings.token_algorithm])
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        
    except JWTError:
        raise  credentials_exception
    
    return token_data
    
def get_current_user(token: Depends(oath2_scheme)):
    '''
    Take the token from request automatically, 
    extract id,
    verify that token is correct,
    add as paramater to path operation funct
    
    A server using HTTP authentication will respond with a 401 Unauthorized response to a request for a protected 
    resource. This response must include at least one WWW-Authenticate header and at least one challenge, to indicate
    what authentication schemes can be used to access the resource (and any additional data that each particular scheme
    needs).
    '''
    _detail = f"Could not validate credentials"
    _header = {"WWW-Authenticate": "Bearer"}
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_detail, headers=_header)
    return verify_access_token(token, credentials_exception)
    