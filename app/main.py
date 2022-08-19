from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


# Whenever we start the application, SQLAlchemy will do either one of the folowing:
# 1. If there is a table with the names in models.py, it will do nothing
# 2. Else it will go ahead  and create the tables in Postgres. Check PGAdmin 
models.Base.metadata.create_all(bind=engine)

app  = FastAPI()

@app.get("/")
def root(): 
    return {'message': 'Hello Worldd'}
    
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db)):
    # # stage changes
    # cursor.execute(
    #     """ 
    #     INSERT INTO posts (title, content, published) 
    #     VALUES (%s, %s, %s) 
    #     RETURNING *
    #     """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # # need to commit in order to save
    # conn.commit()
    new_post =  models.Post(**post.dict())
    db.add(new_post) # stage new post and add to db
    db.commit()  # commit to db
    db.refresh(new_post) # retrieve new post and store into the var new_post
    
    return new_post

@app.get('/posts/{id}')
def get_post(id:int, 
             db: Session = Depends(get_db)):
    # cursor.execute(""" 
    #                SELECT * 
    #                FROM posts AS p
    #                WHERE p.id = %s 
    #                """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found.")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,
                db: Session = Depends(get_db)):
    # cursor.execute("""
    #                DELETE FROM posts AS p 
    #                WHERE p.id =  %s 
    #                RETURNING *  
    #                """, (str(id)))
    # deleted_post =  cursor.fetchone()
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
        

@app.put("/posts/{id}")
def update_post(id:int,
                post: schemas.PostCreate,
                db: Session = Depends(get_db)):
    # cursor.execute("""
    #                UPDATE posts
    #                SET title = %s, content = %s, published = %s
    #                WHERE id = %s
    #                RETURNING * 
    #                """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
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
        