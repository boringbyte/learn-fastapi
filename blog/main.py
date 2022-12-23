import uvicorn
from fastapi import FastAPI
from blog import models
from database import engine
from blog.routers import blog, user


app = FastAPI()
models.Base.metadata.create_all(engine)
app.include_router(blog.router)
app.include_router(user.router)


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
