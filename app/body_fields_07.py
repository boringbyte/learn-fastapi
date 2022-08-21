"""
    - Field is imported from pydantic similar to Required
        - default
        - title
        - max_length
        - min_length
        - gt
        - lt
        - ge
        - le
    - Extra keys passed to Field will also be present in the resulting OpenAPI schema for your application.
"""
import uvicorn
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, title="The description of the item", max_length=300)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
