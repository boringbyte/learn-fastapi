"""
    - When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.
    - A request body is data sent by the client to your API. A response body is the data your API sends to the client.
    - Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all
      the time.
    - We can declare body, path and query parameters, all at the same time.
    - All the optional rules are very similar to query parameters. If default is defined, then those attributes become
      optional like 'description' and 'tax' in 'Item' Model.
    - Schema is generated in the apidocs at the bottom of the page.
    -The function parameters will be recognized as follows:
        - If the parameter is also declared in the path, it will be used as a path parameter.
        - If the parameter is of a singular type (like int, float, str, etc.) it will be interpreted as a query parameter.
        - If the parameter is declared to be of the type Pydantic model, it will be interpreted as a request body.
"""
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
