from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models import BillLine


class BillRepository(ABC):

    @abstractmethod
    def find_bill_lines_by_bill_id(self, bill_id: str):
        pass