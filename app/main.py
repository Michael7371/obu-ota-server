from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from app import manifest
import os
import glob
from fastapi import HTTPException

app = FastAPI()


@app.get("/")
def read_root(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}

@app.get("/firmwares")
def get_manifest(request: Request):
    try:
        files = glob.glob("/firmwares/*.tar.sig")
        print(files)
        host_name = os.getenv("SERVER_NAME","localhost")
        response_manifest = manifest.add_contents(host_name, files)
        print(response_manifest)
        return response_manifest
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/firmwares/{firmware_id}")
def get_fw(firmware_id: str):
    return FileResponse(f"/firmwares/{firmware_id}")

