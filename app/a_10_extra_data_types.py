"""
    - Common data types are:
        - int
        - float
        - str
        - book
    - Complex data types are:
        - UUID
        - datetime.datetime
        - datetime.date
        - datetime.time
        - frozenset
        - bytes
        - Decimal
        - https://pydantic-docs.helpmanual.io/usage/types/
"""
import uvicorn
from uuid import UUID
from fastapi import FastAPI, Body
from datetime import datetime, time, timedelta


app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(item_id: UUID,
                     start_datetime: datetime | None = Body(default=None),
                     end_datetime: datetime | None = Body(default=None),
                     repeat_at: time | None = Body(default=None),
                     process_after: timedelta | None = Body(default=None)):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration}

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
