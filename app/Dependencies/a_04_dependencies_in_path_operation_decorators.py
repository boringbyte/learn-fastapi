"""
    In some cases you don't really need the return value of a dependency inside your path operation function.
    Or the dependency doesn't return a value. But you still need it to be executed/solved.
    For those cases, instead of declaring a path operation function parameter with Depends, you can add a list of
    dependencies to the path operation decorator.
    It should be a list of 'Depends()': These dependencies will be executed/solved the same way normal dependencies.
        But their value (if they return any) won't be passed to your path operation function.
    And they can return values or not, the values won't be used.
"""
import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
