"""
    Steps for creating fast-api application
        1. Import FastAPI class from fastapi library.
        2. Create an instance of FastAPI class which can be app or my_app or anything else.
        3. Create path operation decorator like .get, .post etc. using the instance that we created.
        4. Define the path operation function.
            path is /
            operation is get
            function: is the function below the "decorator" (below @app.get('/')).
        5. Return the content.
"""
import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
