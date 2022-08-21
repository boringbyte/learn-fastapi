"""
    - You can define Cookie parameters the same way you define Query and Path parameters.
    - Cookie is a "sister" class of Path and Query. It also inherits from the same common Param class.
"""
import uvicorn
from fastapi import Cookie, FastAPI


app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
