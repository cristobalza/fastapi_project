from typing import List
from .. import schemas, models, oath2
from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts", 
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user: dict = Depends(oath2.get_current_user)):
    
    # print(current_user.email)        
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: dict = Depends(oath2.get_current_user)):

    new_post =  models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post) # stage new post and add to db
    db.commit()  # commit to db
    db.refresh(new_post) # retrieve new post and store into the var new_post
    
    return new_post

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id:int, 
             db: Session = Depends(get_db),
             current_user: dict = Depends(oath2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # No post in db, no action
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found.")
        
    # If current user's id does not match with the creator/owner id of the post, then deny action
    if post.owner_id != current_user.id:
        _detail=f"Not auhorized to perform requested action."
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=_detail)
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,
                db: Session = Depends(get_db),
                current_user: dict = Depends(oath2.get_current_user)):
    
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # No post in db, no action
    if post is None:
        message = f"id post : {id} was not found."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)
        
    # If current user's id does not match with the creator/owner id of the post, then deny action
    if post.owner_id != current_user.id:
        _detail=f"Not auhorized to perform requested action."
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=_detail)
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        

@router.put("/{id}", response_model=schemas.PostOut)
def update_post(id:int,
                new_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: dict = Depends(oath2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # No post in db, no action
    if post is None:
        message = f"id post : {id} was not found."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)
    
    # If current user's id does not match with the creator/owner id of the post, then deny action
    if post.owner_id != current_user.id:
        _detail=f"Not auhorized to perform requested action."
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=_detail)
    
    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()