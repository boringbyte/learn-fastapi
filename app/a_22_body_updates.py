"""
    - PUT: to update an item you can use this
    - PATCH: to partially update data
    - If you want to receive partial updates, it's very useful to use the parameter exclude_unset in
      Pydantic's model's .dict().
    - Like item.dict(exclude_unset=True). That would generate a dict with only the data that was set when creating
      the item model, excluding default values.
    - Using Pydantic's update parameter. Now, you can create a copy of the existing model using .copy(), and pass the
      update parameter with a dict containing the data to update.
    - https://fastapi.tiangolo.com/tutorial/body-updates/
"""
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
