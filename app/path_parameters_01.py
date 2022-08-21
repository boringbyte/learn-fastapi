"""
    * We can declare path "parameters" or "variables" with the same syntax used by Python format strings:
    * Path parameters with types gives us editor support inside the function, with error checks, completion, etc.
      Type declaration gives us automatic request "parsing".
    * This also helps with data validation. All the data validation is performed under the hood by Pydantic.
    * Create an Enum class. You could also access the value "lenet" with ModelName.lenet.value.
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
