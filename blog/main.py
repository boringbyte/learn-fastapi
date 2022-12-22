import uvicorn
from fastapi import FastAPI
from blog.schemas import Blog

app = FastAPI()


@app.post('/blog')
def create(request: Blog):
    return request


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
