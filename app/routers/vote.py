from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import oath2
from ..database import get_db

router = APIRouter(
    tags=['Vote'],
    prefix='vote'
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(db: Session = Depends(get_db),
                current_user: dict = Depends(oath2.get_current_user)):
    pass