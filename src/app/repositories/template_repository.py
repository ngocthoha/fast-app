from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models import Template


class TemplateRepository(ABC):

    @abstractmethod
    def find_active_templates(self, bill_type: str, term_start_date: str) -> List[Template]:
        pass
    
    @abstractmethod
    def find_default_template_by_type(self, type: str) -> Optional[Template]:
        pass
