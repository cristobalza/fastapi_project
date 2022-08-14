from random import randrange
from fastapi import FastAPI
from fastapi.params import Body
from post import Post

app  = FastAPI()

my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
            {'title': 'favorite foods', 'content': 'I like pizza', 'id': "2"}]

@app.get("/")
def root(): 
    return {'message': 'Hello Worldd'}

@app.get("/posts")
def get_posts():
    return {'data': my_posts}

@app.post("/posts")
def create_posts(post: Post):
    temp = post.dict()
    temp['id'] = randrange(0, 9999999)
    my_posts.append(temp)
    return {'data': temp}

@app.get('/posts/{id}')
def get_post(id:int):
    p = find_post(int(id))
    return {'post_detail': f'this is your post {p}'}

def find_post(id):
    for p in my_posts:
        if int(p['id']) == id:
            return p