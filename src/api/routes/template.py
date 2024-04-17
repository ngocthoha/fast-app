import logging
import os
import shutil
import zipfile
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing_extensions import Annotated

from src.app.services import CommandBus
from src.app.use_cases.template import CreateTemplateCommand
from src.dependencies import get_command_bus

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
    type: Annotated[str, Form()],
    name: Annotated[str, Form()],
    start_date: Annotated[str, Form()],
    end_date: Optional[str] = Form(None),
    file: UploadFile = File(...),
    bus: CommandBus = Depends(get_command_bus),
):
    command = CreateTemplateCommand(
        type=type, name=name, start_date=start_date, end_date=end_date
    )
    try:
        template = bus.execute(command)
        directory = f"src/templates/{type}/{template.id}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_location = f"{directory}/{os.path.basename(file.filename)}"
        with open(file_location, "wb") as f:
            while chunk := file.file.read(CHUNK_SIZE):
                f.write(chunk)

        with zipfile.ZipFile(file_location, "r") as zip_ref:
            zip_ref.extractall(directory)

        def move_to_main(source, destination):
            files = os.listdir(source)
            for file in files:
                file_name = os.path.join(source, file)
                shutil.move(file_name, destination)

        original_filename = f"{directory}/{file.filename[:-4]}"
        move_to_main(original_filename, directory)
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        os.remove(file_location)
        os.rmdir(original_filename)

    return {"message": f"Successfully uploaded {file.filename}"}
