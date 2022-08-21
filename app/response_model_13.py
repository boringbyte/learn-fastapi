"""
    - Use the path operation decorator's parameter response_model to define response models and especially to ensure
      private data is filtered out.
    - You can declare the model used for the response with the parameter response_model in any of the path operations:
        - @app.get()
        - @app.post()
        - @app.put()
        - @app.delete()
        - etc
    - response_model is a parameter of the decorator method.
    - The response model is declared in this parameter instead of as a function return type annotation, because the
      path function may not actually return that response model but rather return a dict, database object or some other
      model, and then use the response_model to perform the field limiting and serialization.
    - pip install email-validator or pip install pydantic[email]
    - You can set the path operation decorator parameter response_model_exclude_unset=True and those default values
      won't be included in the response, only the values actually set.
    - FastAPI uses Pydantic model's .dict() with its exclude_unset parameter to achieve this.
        - response_model_exclude_defaults=True
        - response_model_exclude_none=True
"""
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item


# Don't do this in production!
@app.post("/user1/", response_model=UserIn)
async def create_user1(user: UserIn):
    return user


@app.post("/user2/", response_model=UserOut)
async def create_user2(user: UserIn):
    return user

items = {
    "foo": {"name": "Foo", "price": 50.2},  # calling with foo, doesn't return default values due to response_m_e_u
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/name", response_model=Item, response_model_include=["name", "description"])
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude=["tax"])
async def read_item_public_data(item_id: str):
    return items[item_id]

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
