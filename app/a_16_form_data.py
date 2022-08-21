"""
    - To use forms, first install python-multipart
    - Create form parameters the same way you would for Body or Query:
    - Use Form to declare form data input parameters.
"""
import uvicorn
from fastapi import FastAPI, Form


app = FastAPI()


@app.post("/login")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
