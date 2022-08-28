from typing import List, Optional
from .. import schemas, models, oath2
from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db

router = APIRouter(
    prefix="/posts", 
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOutVote])
def get_posts(db: Session = Depends(get_db), 
              current_user: dict = Depends(oath2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):
    
    # list_posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id ).all()
    list_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(type(list_posts))
    # print(type(list_posts[0]))
    
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id)

    
    # print(results)
    # return results.all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: dict = Depends(oath2.get_current_user)) -> models.Post:

    new_post =  models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post) # stage new post and add to db
    db.commit()  # commit to db
    db.refresh(new_post) # retrieve new post and store into the var new_post
    return new_post

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id:int, 
             db: Session = Depends(get_db),
             current_user: dict = Depends(oath2.get_current_user)) -> models.Post:
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # No post in db, no action
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found.")
    
    # If current user's id does not match with the creator/owner id of the post, then deny action
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not auhorized to perform requested action.")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,
                db: Session = Depends(get_db),
                current_user: dict = Depends(oath2.get_current_user)) -> Response:
    
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # No post in db, no action
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id post : {id} was not found.")
        
    # If current user's id does not match with the creator/owner id of the post, then deny action
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not auhorized to perform requested action.")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        

@router.put("/{id}", response_model=schemas.PostOut)
def update_post(id:int,
                new_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: dict = Depends(oath2.get_current_user)) -> models.Post:
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # print(type(post_query))
    post = post_query.first()
    # print(type(post))
    
    # No post in db, no action
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id post : {id} was not found.")
    
    # If current user's id does not match with the creator/owner id of the post, then deny action
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not auhorized to perform requested action.")
    
    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

################################
# Documentation: 
# Retrieving posts using Raw SQL on Postgres
################################
# from ..database import cursor, conn
# @router.get("/posts")
# def get_posts():
#     cursor.execute(""" SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {'data': posts}

# @router.post("/posts", status_code = status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     # stage changes
#     cursor.execute(""" INSERT INTO posts (title, content, published) 
#                         VALUES (%s, %s, %s) RETURNING *
#                     """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     # need to commit in order to save
#     conn.commit()
#     return {'data': new_post}

# @router.get('/posts/{id}')
# def get_post(id:int, response: Response):
#     cursor.execute(""" SELECT * FROM posts AS p WHERE p.id = %s 
#                    """, (str(id)))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id : {id} was not found.")
#     return {'post_detail': f'this is your post {post}'}

# @router.delete("/posts/{id}")
# def delete_post(id:int, status_code=status.HTTP_204_NO_CONTENT):
#     cursor.execute("""DELETE FROM posts AS p 
#                       WHERE p.id =  %s 
#                       RETURNING *  
#                     """, (str(id)))
#     deleted_post =  cursor.fetchone()
#     if deleted_post is not None:
#         conn.commit() # every time we make a change to db
#         return Response(status_code=status.HTTP_204_NO_CONTENT)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id post : {id} was not found.")
# 
# @router.put("/posts/{id}")
# def update_post(id:int, post: Post):
#     cursor.execute("""UPDATE posts
#                       SET title = %s, content = %s, published = %s
#                       WHERE id = %s
#                       RETURNING * 
#                     """, (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post is not None:
#         return {'data': updated_post}
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id post : {id} was not found.")
################################