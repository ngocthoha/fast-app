import uuid
from typing import List, Optional

from src.app.repositories import TemplateRepository
from src.domain.models import Template


class SQLTemplateRepository(TemplateRepository):
    def __init__(self, session):
        self.session = session

    def generate_id(self) -> str:
        return str(uuid.uuid4())

    def find_active_templates(
        self, bill_type: str, term_start_date: str
    ) -> List[Template]:
        query = self.session.query(Template).filter(
            Template.type == bill_type,
            Template.start_date <= term_start_date,
        )
        return query.all()

    def find_default_template_by_type(self, type: str) -> Optional[Template]:
        template = (
            self.session.query(Template)
            .filter(
                Template.type == type,
                Template.start_date._is(None),
                Template.end_date._is(None),
            )
            .first()
        )
        return template

    def save(self, template: Template):
        self.session.add(template)
