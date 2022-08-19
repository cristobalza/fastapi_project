from typing import List
from .. import schemas, models
from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.get("/posts", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db)):
    new_post =  models.Post(**post.dict())
    db.add(new_post) # stage new post and add to db
    db.commit()  # commit to db
    db.refresh(new_post) # retrieve new post and store into the var new_post
    
    return new_post

@router.get('/posts/{id}', response_model=schemas.PostOut)
def get_post(id:int, 
             db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found.")
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,
                db: Session = Depends(get_db)):
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        message = f"id post : {id} was not found."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)
    else:
        # conn.commit() # every time we make a change to db
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        

@router.put("/posts/{id}", response_model=schemas.PostOut)
def update_post(id:int,
                post: schemas.PostCreate,
                db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        message = f"id post : {id} was not found."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)
    else:
        post_query.update(post.dict(), 
                          synchronize_session=False)
        db.commit()
        return post_query.first()