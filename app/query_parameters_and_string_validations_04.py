"""
    - Additional query parameter validations can be done using Query
    - default
    - min_length
    - max_length
    - regex
    - ... can used to make it required or using Required class from pydantic
        Eg: Query(default=..., min_length=3) or Query(default=Required, min_length=3)
    - Remember that in most of the cases, when something is required, you can simply omit the default parameter,
      so you normally don't have to use ... nor Required.
    - title
    - description
    - alias
    - deprecated=True
    - include_in_schema=True
"""
import uvicorn
from fastapi import FastAPI, Query
from pydantic import Required


app = FastAPI()


@app.get("/items1/")
async def read_items1(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items2/")
async def read_items2(q: str | None = Query(default=Required, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(q: list[str] = Query(default=["foo", "bar"], title="Query String",
                                          description="Query string for the items to search in the "
                                                      "database that have a good match",
                                          alias="item-query"
                                          )):
    query_items = {"q": q}
    return query_items


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
