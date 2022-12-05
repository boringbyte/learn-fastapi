"""
    * We can declare path "parameters" or "variables" with the same syntax used by Python format strings:
    * Path parameters with types gives us, editor support inside the function, with error checks, completion, etc.
      Type declaration gives us automatic request "parsing".
    * This also helps with data validation. All the data validation is performed under the hood by Pydantic.
      If you pass '3' instead of 3 to read_item, we will see type_error.integer.
      Same thing happens if we pass float instead of int. All the validation under the hood are performed by pydantic.
    * Order matters, when creating path operations. '/users/me', '/users/{user_id} are defined in order, then for any
      input value, the api will not call '/users/{user_id}' as it would match '/users/me 'as well, thinking that it's
      receiving a parameter user_id with a value of 'me'.
    * Create an Enum class for predefined values. This will provide us with drop down selection in the apidocs.
      By inheriting from str the API docs will be able to know that the values must be of type string and will be able to render correctly.
      You could also access the value "lenet" with ModelName.lenet.value.
    * Path parameters containing paths. Using an option directly from Starlette you can declare a path parameter
      containing a path using a URL like below. In this case, the name of the parameter is file_path, and the last part,
      :path, tells it that the parameter should match any path.
"""
import uvicorn
from fastapi import FastAPI
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
