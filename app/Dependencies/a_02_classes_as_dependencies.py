"""
In the previous example, we were returning a dict from our dependency ("dependable"):
The key factor is that a dependency should be a "callable".
A "callable" in Python is anything that Python can "call" like a function.
So, if you have an object something (that might not be a function) and you can "call" it (execute it) like:
But you see that we are having some code repetition here, writing CommonQueryParams twice:
Instead of writing:
    commons: CommonQueryParams = Depends(CommonQueryParams)
...you write:
    commons: CommonQueryParams = Depends()
"""
import uvicorn
from fastapi import FastAPI, Depends

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
