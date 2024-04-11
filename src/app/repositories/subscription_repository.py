from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models import Bill


class SubscriptionRepository(ABC):

    @abstractmethod
    def find_subscriptions_by_(self, bill_id: str) -> Optional[Bill]:
        pass