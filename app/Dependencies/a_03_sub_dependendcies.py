"""
    You can create dependencies that have sub-dependencies. They can be as deep as you need them to be.
    If one of your dependencies is declared multiple times for the same path operation, for example, multiple dependencies
    have a common sub-dependency, FastAPI will know to call that sub-dependency only once per request.
"""
import uvicorn
from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(q: str = Depends(query_extractor), last_query: str | None = Cookie(default=None)):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: query_or_cookie_extractor = Depends()):
    return {"q_or_cookie": query_or_default}

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
