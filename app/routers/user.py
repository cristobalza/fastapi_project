from .. import schemas, models, utils
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['User']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate,
                 db: Session = Depends(get_db)):
    # hash password - user.password and update the pydantic User model
    hash_password = utils.hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()  
    db.refresh(new_user) 
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        message=f'User with id : {id} does not exists.'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    else:
        return user