from datetime import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.app.services import CommandBus
import aiofiles
import os
from src.app.use_cases.template import CreateTemplateCommand
from src.dependencies import get_command_bus
from fastapi.templating import Jinja2Templates


CHUNK_SIZE = 1024 * 1024

templates = Jinja2Templates(directory="bills")
router = APIRouter()


class CreateTemplateRequest(BaseModel):
    type: str
    name: str
    start_date: str
    end_date: str


@router.post("")
async def create_template(
    # body: CreateTemplateRequest,
    file: UploadFile = File(...),
    bus: CommandBus = Depends(get_command_bus),
):
    # command = CreateTemplateCommand(type=body.type, name=body.name, start_date=body.start_date, end_date=body.end_date)
    try:
        # template = bus.execute(command)
        filepath = os.path.join('./', os.path.basename(file.filename))
        print(filepath)
        with open(filepath, 'wb') as f:
            while chunk := file.file.read(CHUNK_SIZE):
                f.write(chunk)
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        file.close()
    # return templates.TemplateResponse("bd416a7e-1bec-45be-955f-b101c3375e12.pdf", context= {"request": request}) 
    return FileResponse(template, media_type='application/pdf')
