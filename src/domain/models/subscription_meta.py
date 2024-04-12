import attrs
from src.domain.models.subscription import Subscription


@attrs.define(slots=False, kw_only=True)
class SubscriptionMeta:
    id: str
    init_quantity: int
    subscription: Subscription
    subscription_id: str
