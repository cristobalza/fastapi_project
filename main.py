from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from post import Post

app  = FastAPI()

my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
            {'title': 'favorite foods', 'content': 'I like pizza', 'id': 2}]

@app.get("/")
def root(): 
    return {'message': 'Hello Worldd'}

@app.get("/posts")
def get_posts():
    return {'data': my_posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    temp = post.dict()
    temp['id'] = randrange(0, 9999999)
    my_posts.append(temp)
    return {'data': temp}

@app.get('/posts/{id}')
def get_post(id:int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found.")
    return {'post_detail': f'this is your post {post}'}

@app.delete("/posts/{id}")
def delete_post(id:int, status_code=status.HTTP_204_NO_CONTENT):
    # deleting post
    # find index in the array that has requried id
    # my_posts.pop(index)
    index = find_index(id)
    if index is not None:
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id post : {id} was not found.")

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    index = find_index(id)
    if index is not None:
        temp = post.dict()
        temp['id'] = id
        my_posts[index] = temp
        return{'data': temp}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id post : {id} was not found.")



def find_post(id:int):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id:int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None