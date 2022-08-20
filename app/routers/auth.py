from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credentials: schemas.UserLogin, 
          db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if user is None:
        message = f"Invalid credentials."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    # compare attempted password's hash with the user.email hash
    if utils.verify(user_credentials.password, user.password) is False:
        message = f"Invalid credentials."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    
    # create a token
    return {'token': 'example token'}
    