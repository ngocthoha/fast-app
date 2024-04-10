from src.adapters.repositories import SQLBillRepository
from src.app.services import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.bill_repository = SQLBillRepository(self.session)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
