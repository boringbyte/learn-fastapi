"""
    - We can declare an example for a Pydantic model using Config and schema_extra.
    - When using Field() with Pydantic models, you can also declare extra info for the JSON Schema by passing any other
      arbitrary arguments to the function.
    - Keep in mind that those extra arguments passed won't add any validation, only extra information, for documentation
      purposes.
    - Path(), Query(), Header(), Cookie(), Body(), Form(), File()
    - Multiple examples can be added to Body
        - examples can be passed using dict with multiple examples.
        - dict in the examples contain below keys:
            - summary: Short description for the example.
            - description: A long description that can contain Markdown text.
            - value: This is the actual example shown, e.g. a dict.
            - externalValue: alternative to value, a URL pointing to the example.
              Although this might not be supported by as many tools as value.
"""
import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field


app = FastAPI()


class Item1(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2
            }
        }


class Item3(BaseModel):
    name: str = Field(example="Foo")
    description: str | None = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: float | None = Field(default=None, example=3.2)


@app.put("/items1/{item_id}")
async def update_item1(item_id: int, item: Item1 = Body(example={"name": "Foo", "description": "A very nice Item",
                                                                 "price": 35.4, "tax": 3.2})):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items2/{item_id}")
async def update_item2(item_id: int, item: Item2):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items3/{item_id}")
async def update_item3(item_id: int, item: Item3):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items4/{item_id}")
async def update_item4(
    *,
    item_id: int,
    item: Item1 = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
