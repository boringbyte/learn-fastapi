"""
    - You could also use from starlette import status.
    - FastAPI provides the same starlette.status as fastapi.status just as a convenience for you, the developer.
      But it comes directly from Starlette.
"""
import uvicorn
from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
