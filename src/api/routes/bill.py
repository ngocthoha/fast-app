import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.app.services import CommandBus
from src.app.use_cases.bill import (
    GetBillCommand,
)
from src.app.use_cases.processors.render_tempate import RenderTemplateCommand
from src.dependencies import get_command_bus
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="bills")
router = APIRouter()


# @router.get("/{id}")
# def get_bill(
#     id: str,
#     bus: CommandBus = Depends(get_command_bus),
# ):
#     command = GetBillCommand(bill_id=id)
#     try:
#         bill = bus.execute(command)
#     except Exception as e:
#         logging.exception(e)
#         raise HTTPException(status_code=500, detail="Internal server error")
#     return bill


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
    return FileResponse("D:\\BizflyCloud\\fast-app\\bills\\bd416a7e-1bec-45be-955f-b101c3375e12.cloud_server.bill.pdf", media_type='application/pdf')