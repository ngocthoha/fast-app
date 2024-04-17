from src.app.services.unit_of_work import UnitOfWork
from dataclasses import dataclass


@dataclass
class CreateTemplateCommand:
    type: str
    name: str
    start_date: str
    end_date: str


class CreateTemplateUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def execute(self):
        with self._uow:
            pass