"""
    - Continuing with the previous example, it will be common to have more than one related model.
    - This is especially the case for user models, because:
        - The input model needs to be able to have a password.
        - The output model should not have a password.
        - The database model would probably need to have a hashed password.
    - You can declare a response to be the Union of two types, that means, that the response would be any of the two.
      It will be defined in OpenAPI with anyOf.
"""
import uvicorn
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    # UserInDB(
    #     username=user_dict["username"],
    #     password=user_dict["password"],
    #     email=user_dict["email"],
    #     full_name=user_dict["full_name"],
    #     hashed_password=hashed_password,
    # )
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


class Item(BaseModel):
    name: str
    description: str


items1 = [{"name": "Foo", "description": "There comes my hero"}, {"name": "Red", "description": "It's my aeroplane"}]


@app.get("/items/", response_model=list[Item])
async def read_items():
    return items1


@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
