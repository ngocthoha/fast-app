import logging
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing_extensions import Annotated

from src.app.services import CommandBus
from src.app.use_cases.template import CreateTemplateCommand
from src.dependencies import get_command_bus

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
        file=file, type=type, name=name, start_date=start_date, end_date=end_date
    )
    try:
        template = bus.execute(command)

    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"message": f"Successfully uploaded {template.name}"}
