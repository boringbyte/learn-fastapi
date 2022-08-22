"""
    - status_code
    - tags: They will be added to the OpenAPI schema and used by the automatic documentation interfaces.
      If you have a big application, you might end up accumulating several tags, and you would want to make sure you
      always use the same tag for related path operations.
    - summary and description
    - docstring: As descriptions tend to be long and cover multiple lines, you can declare the path operation
      description in the function docstring and FastAPI will read it from there.
    - response description: Notice that response_description refers specifically to the response, the description
      refers to the path operation in general.
    - deprecated: True/False Check how deprecated and non-deprecated path operations look like:
    -
"""
import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


class Tags(Enum):
    items = "items"
    users = "users"


@app.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal keys", "Plumbus"]


@app.get("/users/", tags=[Tags.users])
async def read_user():
    return ["Rick", "Morty"]


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED,
          tags=["items"], summary="Create an item", description="Create an item with all the info",
          response_description="The created item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
