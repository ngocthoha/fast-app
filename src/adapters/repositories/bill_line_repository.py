from src.app.repositories.bill_line_repository import BillLineRepository
from src.domain.models.bill import Bill
from src.domain.models.bill_line import BillLine
from src.domain.models.subscription import Subscription


class SQLBillLineRepository(BillLineRepository):
    def __init__(self, session):
        self.session = session

    def find_bill_lines_by_bill_id(self, bill_id: str):
        query = (
            self.session.query(BillLine)
            .join(Bill)
            .join(Subscription)
            .filter(Bill.id == bill_id)
        )
        return query.all()
