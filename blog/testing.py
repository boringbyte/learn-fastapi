import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get('/')
async def root():
    return {'data': 'blog list'}


@app.get('/blog/{blog_id}')
async def show(blog_id: int):
    return {'data': blog_id}


@app.get('/blog/{blog_id}/comments')
def comments(blog_id):
    return {'data': {'1', '2'}}


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
