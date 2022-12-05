"""
    - Validations are valid for both Path and Query class. Both String and Numeric validations.
    - When you import Query, Path and others from fastapi, they are actually functions.
    - That when called, return instances of classes of the same name.
    - A path parameter is always required as it has to be part of the path.
        - title
        - ge --> greater than or equal to
        - le
        - gt --> greater than
        - lt
        - These validations can be used for number type in Query parameters as well.
    - Order the parameters as you need
    - Order the parameters as you need, tricks.
        - If you want to declare the q query parameter without a Query nor any default value, and the path parameter
          item_id using Path, and have them in a different order, Python has a little special syntax for that.
        - Pass *, as the first parameter of the function.
        - Python won't do anything with that *, but it will know that all the following parameters should be called as
          keyword arguments (key-value pairs), also known as kwargs. Even if they don't have a default value.
    - Query, Path, and others are subclasses of a common Param class. All of them share the same all these same
      parameters of additional validation and metadata you have seen.
    - When you import Query, Path and others from fastapi, they are actually functions. That when called, return
      instances of classes of the same name.
"""
import uvicorn
from fastapi import Query, Path, FastAPI


app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(*,
                     item_id: str = Path(title="The ID of the item to get"),
                     q: str | None = Query(default=None, alias="item-query"),
                     size: float = Query(gt=0, lt=10.5)):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    results.update({"size": size})
    return results


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
