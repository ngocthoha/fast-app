from dataclasses import dataclass
from src.app.services.unit_of_work import UnitOfWork
from src.adapters.services import PDFBillProcessor



@dataclass
class RenderTemplateCommand:
    bill_id: str
    type: str


class RenderTemplateUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def execute(self, command: RenderTemplateCommand):
        return PDFBillProcessor.generate_template(
            command.bill_id, command.type
        )