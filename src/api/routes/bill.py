import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from src.app.services import CommandBus
from src.app.use_cases.processors.render_tempate import RenderTemplateCommand
from src.dependencies import get_command_bus

templates = Jinja2Templates(directory="bills")
router = APIRouter()


@router.get("/{id}")
def generate_template(
    id: str,
    request: Request,
    type: str = "PDF",
    bus: CommandBus = Depends(get_command_bus),
):
    command = RenderTemplateCommand(bill_id=id, type=type)
    try:
        template = bus.execute(command)
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    # return templates.TemplateResponse("bd416a7e-1bec-45be-955f-b101c3375e12.pdf", context= {"request": request})
    return FileResponse(template, media_type="application/pdf")
