from dataclasses import dataclass

import attrs
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
        bill_lines = self._uow.bill_line_repository.find_bill_lines_by_bill_id(
            command.bill_id
        )
        bill_lines = attrs.asdict(bill_lines)
        pdf_bill_processor = PDFBillProcessor()
        return pdf_bill_processor.generate_template(
            command.bill_id, command.type
        )