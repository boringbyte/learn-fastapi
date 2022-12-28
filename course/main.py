import sys
import time
import uvicorn
import psycopg2
from fastapi import FastAPI, status, Response, HTTPException
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

i = 3
current_try, tries = 0, 5
app = FastAPI()
my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
            {'title': 'title of post 2', 'content': 'content of post 2', 'id': 2}]

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres',
                                cursor_factory=RealDictCursor)
        print('Postgres "fastapi" database connection was successful')
        break
    except Exception as e:
        print(f'Failed to connect to Postgres Database with error: {e}')
        time.sleep(2)
        current_try += 1
    if current_try == tries:
        print(f'Failed to connect to Postgres Database for {current_try} times. So, closing the app completely')
        sys.exit(0)


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


def find_post_index(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None


@app.get('/')
async def root():
    return {'message': 'Hello World!'}


@app.get('/posts')
async def get_posts():
    return my_posts


@app.get('/posts/{id}')
async def get_post(id: int):
    return {id: f'this is test post {id}'}


# from fastapi.params import Body
# payload: dict = Body(...) Extract body from the message body which do not use pydantic base model and that sends json
# or dictionary message body.
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    global i
    post_dict = post.dict()
    post_dict['id'] = i
    my_posts.append(post_dict)
    i += 1
    return {'new_post': post.dict()}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
async def update_post(id: int, updated_post: Post):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')
    updated_post_dict = updated_post.dict()
    updated_post_dict['id'] = id
    my_posts[index] = updated_post_dict
    return {'data': updated_post}


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
