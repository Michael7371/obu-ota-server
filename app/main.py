from typing import Union
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import StreamingResponse, FileResponse
from app import manifest
import os
import glob
import aiofiles
from starlette.responses import Response
import logging

app = FastAPI()
log_level = (
        "INFO" if "LOGGING_LEVEL" not in os.environ else os.environ["LOGGING_LEVEL"]
    )

logging.basicConfig(format="%(levelname)s:%(message)s", level=log_level)

async def file_iterator(file_path: str):
    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            yield chunk

@app.get("/")
def read_root(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}

@app.get("/firmwares")
def get_manifest(request: Request):
    try:
        files = glob.glob("/firmwares/*.tar.sig")
        logging.debug(files)
        host_name = os.getenv("SERVER_HOST","localhost")
        response_manifest = manifest.add_contents(host_name, files)
        logging.debug(response_manifest)
        return response_manifest
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/firmwares/{firmware_id}")
async def get_fw(request: Request, firmware_id: str):
    logging.debug(f"Method: {request.method}")
    logging.debug(f"URL: {request.url}")
    logging.debug(f"Headers: {request.headers}")
    logging.debug(f"Query Parameters: {request.query_params}")
    logging.debug(f"Client: {request.client}")
    logging.debug(f"Cookies: {request.cookies}")
    file_path = f"/firmwares/{firmware_id}"
    range_header = request.headers.get('Range')
    start, end = 0, None

    if range_header:
        start_end = range_header.partition('=')[2].split('-')
        start = int(start_end[0])
        end = int(start_end[1]) if start_end[1] else None

    async with aiofiles.open(file_path, mode='rb') as file:
        file_size = os.path.getsize(file_path)
        if end is None:
            end = file_size
        await file.seek(start)
        data = await file.read(end - start)

    headers = {
        'Content-Range': f'bytes {start}-{end-1}/{file_size}',
        'Content-Length': str(end - start),
        'Accept-Ranges': 'bytes',
    }

    logging.debug(f"Completed Firmware Response for lient: {request.client}")
    return Response(content=data, media_type='application/octet-stream', headers=headers)
    