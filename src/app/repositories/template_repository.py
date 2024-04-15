from abc import ABC, abstractmethod
from typing import List
from src.domain.models import Template


class TemplateRepository(ABC):

    @abstractmethod
    def find_active_templates(self, bill_type: str) -> List[Template]:
        pass
