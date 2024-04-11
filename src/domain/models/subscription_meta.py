from domain.models.subscription import Subscription


class SubscriptionMeta:
    id: str
    init_quantity: int
    subscription: Subscription
