"""
    - There are some cases where you might need to convert a data type (like a Pydantic model) to something compatible
      with JSON (like a dict, list, etc).
    - For example, if you need to store it in a database. For that, FastAPI provides a jsonable_encoder() function
"""
import uvicorn
from datetime import datetime
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_database = {}
app = FastAPI()


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_database[id] = json_compatible_item_data


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
