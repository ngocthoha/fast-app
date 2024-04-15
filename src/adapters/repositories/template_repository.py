from typing import List
from src.app.repositories import TemplateRepository
from src.domain.models import Template


class SQLTemplateRepository(TemplateRepository):

    def __init__(self, session):
        self.session = session

    def find_active_templates(self, bill_type: str) -> List[Template]:
        query = (
            self.session.query(Template)
            .filter(Template.type == bill_type)
        )
        return query.all()