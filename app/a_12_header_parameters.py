"""
    - You can define Cookie parameters the same way you define Query and Path parameters.
    - Header is a "sister" class of Path and Query. It also inherits from the same common Param class.
    - Header has a little extra functionality on top of what Path, Query and Cookie provide.
    - Most of the standard headers are separated by a "hyphen" character, also known as the "minus symbol" (-).
      But a variable like user-agent is invalid in Python.
        - convert_underscores=False
    - Before setting convert_underscores to False, bear in mind that some HTTP proxies and servers disallow the usage
      of headers with underscores.
    - It is possible to receive duplicate headers. That means, the same header with multiple values.
"""
import uvicorn
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items1/")
async def read_items1(user_agent: str | None = Header(default=None, convert_underscores=False)):
    return {"User-Agent": user_agent}


@app.get("/items2/")
async def read_items2(x_token: list[str] | None = Header(default=None)):
    return {"X-Token values": x_token}

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
