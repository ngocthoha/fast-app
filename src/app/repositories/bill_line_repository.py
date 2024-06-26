from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.models import BillLine


class BillLineRepository(ABC):
    @abstractmethod
    def find_bill_lines_by_bill_id(self, bill_id: str):
        pass
