from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models import Bill


class TemplateRepository(ABC):

    @abstractmethod
    def find_active_template(self, bill_type: str) -> Optional[Bill]:
        pass