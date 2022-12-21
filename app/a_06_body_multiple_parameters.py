"""
    - Body parameters are mostly present when we need to send data to API
    - The same way there is a Query and Path to define extra data for query and path parameters, 
      FastAPI provides an equivalent Body.
    - Body also has all the same extra validation and metadata parameters as Query,Path and others you will see later.
    - You can add multiple body parameters to your path operation function, even though a request can only have a
      single body.

"""
import uvicorn
from fastapi import FastAPI, Path, Body
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items1/{item_id}")
async def update_item1(*,
                       item_id: int = Path(title="The ID of the item to get", ge=0, le=100),
                       q: str | None = None,
                       item: Item | None = None):
    results = {"item_id": item_id}  # path parameter
    if q:
        results.update({"q": q})  # query parameter
    if item:
        results.update({"item": item})  # Body parameter
    return results


@app.put("/items2/{item_id}")
async def update_item2(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


@app.put("/items3/{item_id}")
async def update_item3(item_id: int, item: Item, user: User, importance: int = Body(gt=0)):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


@app.put("/items4/{item_id}")
async def update_item4(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(gt=0),
    q: str | None = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


@app.put("/items5/{item_id}")
async def update_item5(item_id: int, item: Item = Body(embed=True)):
    """
    {
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        }
    }
    instead of 
    {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
    """
    results = {"item_id": item_id, "item": item}
    return results


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
