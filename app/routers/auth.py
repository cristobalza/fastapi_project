from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oath2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(database.get_db)) -> dict:
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # if user is not found in our DB. For this project, email is the username
    if user is None:
        _detail = f"Invalid credentials."
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=_detail)

    # compare attempted password's hash with the user.email hash
    if utils.verify(user_credentials.password, user.password) is False:
        _detail = f"Invalid credentials."
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=_detail)
    
    # create a token
    access_token = oath2.create_access_token(data={"user_id": user.id,
                                                   "user_email": user.email})
    return {'access_token': access_token,
            "token_type": "bearer"}
    