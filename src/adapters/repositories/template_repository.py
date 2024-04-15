from src.domain.models.account import Account
from src.app.repositories import TemplateRepository
from src.domain.models import Bill


class SQLTemplateRepository(TemplateRepository):

    def __init__(self, session):
        self.session = session

    def find_active_template(self, bill_type: str):
        bill = (
            self.session.query(Bill)
            .join(Account)
            .filter(Bill.id == bill_id)
            .first()
        )
        return bill