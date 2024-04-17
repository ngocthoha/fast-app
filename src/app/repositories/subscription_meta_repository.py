from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models import SubscriptionMeta


class SubscriptionMetaRepository(ABC):
    @abstractmethod
    def find_by_subscription_ids(self, subscription_ids: str):
        pass
