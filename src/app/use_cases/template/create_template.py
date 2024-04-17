from dataclasses import dataclass

from src.app.services.unit_of_work import UnitOfWork
from src.domain.models.template import Template


@dataclass
class CreateTemplateCommand:
    type: str
    name: str
    start_date: str
    end_date: str


@dataclass
class CreateTemplateResponse:
    id: str
    type: str
    name: str
    start_date: str
    end_date: str


class CreateTemplateUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def execute(self, command: CreateTemplateCommand):
        from src.dependencies import unit_of_work_custom

        with unit_of_work_custom:
            template_id = unit_of_work_custom.template_repository.generate_id()
            template = Template(
                id=template_id,
                type=command.type,
                name=command.name,
                start_date=command.start_date,
                end_date=command.end_date,
            )
            unit_of_work_custom.template_repository.save(template)
            unit_of_work_custom.commit()

            return CreateTemplateResponse(
                id=template.id,
                type=template.type,
                name=template.name,
                start_date=template.start_date,
                end_date=template.end_date,
            )
