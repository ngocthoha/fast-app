from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models import Bill


class BillRepository(ABC):

    @abstractmethod
    def find_by_id(self, bill_id: str) -> Optional[Bill]:
        pass