from app.repositories.bill_line_repository import BillLineRepository
from domain.models.bill_line import BillLine


class SQLBillLineRepository(BillLineRepository):

    def __init__(self, session):
        self.session = session

    def find_bill_lines_by_bill_id(self, bill_id: str):
        bill_lines = (
            self.session.query(BillLine)
            .filter(BillLine.bill.id == bill_id)
        )
        return bill_lines