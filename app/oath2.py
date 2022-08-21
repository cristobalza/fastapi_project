from datetime import datetime, timedelta
from jose import JWTError, jwt
from .config import settings
from . import schemas, models
from .database import get_db
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.token_secret_key
ALGORITHM = settings.token_algorithm
TOKEN_EXPIRE_MINUTES = settings.token_expiration_time_minutes

def create_access_token(data: dict):
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt  = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, 
                        credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        _id: str = payload.get("user_id")
        # _email: str = payload.get("user_email")   
        if _id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=_id)
    except JWTError as e:
        print(e)
        raise credentials_exception

    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme),
                     db : Session = Depends(get_db)):
    '''
    Take the token from request automatically
    Decode token
    extract id, else throw error
    verify that token is correct, else throw error
    add as paramater to path operation funct
    return token (which is the id)
    
    A server using HTTP authentication will respond with a 401 Unauthorized response to a request for a protected 
    resource. This response must include at least one WWW-Authenticate header and at least one challenge, to indicate
    what authentication schemes can be used to access the resource (and any additional data that each particular scheme
    needs).
    '''
    _detail = f"Could not validate credentials"
    _header = {"WWW-Authenticate": "Bearer"}
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_detail, headers=_header)
    
    token = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user