from abc import ABC, abstractmethod

from ..repositories import BillRepository


class UnitOfWork(ABC):
    bill_repository: BillRepository

    @abstractmethod
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
