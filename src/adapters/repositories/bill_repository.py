from src.domain.models import Account, Service
from src.app.repositories import BillRepository
from src.domain.models import Bill


class SQLBillRepository(BillRepository):

    def __init__(self, session):
        self.session = session

    def find_by_id(self, bill_id: str):
        bill = (
            self.session.query(Bill)
            .join(Account)
            .join(Service)
            .filter(Bill.id == bill_id)
            .first()
        )
        return bill
