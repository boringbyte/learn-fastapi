"""
    - To receive uploaded files, first install python-multipart
    - Files will be uploaded as "form data"
    - If you declare the type of your path operation function parameter as bytes, FastAPI will read the file for you
      and you will receive the contents as bytes.
    - Have in mind that this means that the whole contents will be stored in memory. This will work well for small
      files. But there are several cases in which you might benefit from using UploadFile.
    - Using UploadFile has several advantages over bytes:
        - You don't have to use File() in the default value of the parameter.
        - It uses a "spooled" file. A file stored in memory up to a maximum size limit, and after passing this limit
          it will be stored in disk.
        - This means that it will work well for large files like images, videos, large binaries, etc. without consuming
          all the memory.
        - You can get metadata from the uploaded file.
        - It has a file-like async interface.
        - It exposes an actual Python SpooledTemporaryFile object that you can pass directly to other libraries that
          expect a file-like object.
        - Read https://fastapi.tiangolo.com/tutorial/request-files/ for more information
"""
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes | None = File(default=None)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    return {"filename": file.filename}


@app.post("/files/")
async def create_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
