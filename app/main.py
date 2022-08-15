from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from .post import Post
import psycopg2
from psycopg2.extras import RealDictCursor
import time 


app  = FastAPI()

################################
# Database Connection
################################
while True:
    try:
        conn = psycopg2.connect(host='localhost', 
                                database='fastapi',
                                user='postgres',
                                password='***************',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database was connected succesfully!")
        break
    except Exception as error:
        print("Connecting to Database failed.")
        print(f"Error : {error}")
        time.sleep(3)
################################

@app.get("/")
def root(): 
    return {'message': 'Hello Worldd'}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {'data': posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    # stage changes
    cursor.execute(""" INSERT INTO posts (title, content, published) 
                        VALUES (%s, %s, %s) RETURNING *
                    """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    # need to commit in order to save
    conn.commit()
    return {'data': new_post}

@app.get('/posts/{id}')
def get_post(id:int, response: Response):
    cursor.execute(""" SELECT * FROM posts AS p WHERE p.id = %s 
                   """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found.")
    return {'post_detail': f'this is your post {post}'}

@app.delete("/posts/{id}")
def delete_post(id:int, status_code=status.HTTP_204_NO_CONTENT):
    cursor.execute("""DELETE FROM posts AS p 
                      WHERE p.id =  %s 
                      RETURNING *  
                    """, (str(id)))
    deleted_post =  cursor.fetchone()
    if deleted_post is not None:
        conn.commit() # every time we make a change to db
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id post : {id} was not found.")

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts
                      SET title = %s, content = %s, published = %s
                      WHERE id = %s
                      RETURNING * 
                    """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is not None:
        return {'data': updated_post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id post : {id} was not found.")

###################################
# Helpers
###################################

my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
            {'title': 'favorite foods', 'content': 'I like pizza', 'id': 2}]

def find_post(id:int):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id:int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None