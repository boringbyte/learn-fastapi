import random

import uvicorn
from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
post_database = [{
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "title of post 2",
        "content": "content of post 2",
        "id": 2
    }]

"""
    CRUD --> Create, Read, Update and Delete
    Pydantic provides the base model. 
    {"data": f"title {post.title}, content: {post.content}, published: {post.published},"f"rating: {post.rating}"}
    order of the routes is important as FastAPI scans from top to bottom
    when we crate new item, send 201 HTTP response
    - use hostname:port/docs to view swagger ui
"""


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(pid):
    for post in post_database:
        if pid == post['id']:
            return post


def find_index_post(pid):
    for i, post in enumerate(post_database):
        if post['id'] == pid:
            return pid


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts/{post_id}")  # post_id is called path parameter.
async def get_post(post_id: int):  # path parameter and function argument should be with same name
    print(post_id)
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")
    return {"post_detail": f"Here is the post {post_id}"}


@app.get("/posts")
async def get_posts():
    return {"data": post_database}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = random.randrange(3, 1000000)
    post_database.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    idx = find_index_post(post_id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")
    post_database.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post_id: int, post: Post):
    idx = find_index_post(post_id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")
    post_dict = post.dict()
    post_dict['id'] = post_id
    post_database[idx] = post_dict
    return {"data": post_dict}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
