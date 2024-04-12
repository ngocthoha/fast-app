from src.app.repositories import SubscriptionMetaRepository
from src.domain.models import SubscriptionMeta, Subscription


class SQLSubscriptionMetaRepository(SubscriptionMetaRepository):

    def __init__(self, session):
        self.session = session

    def find_by_subscription_ids(self, subscription_ids: str):
        query = (
            self.session.query(
                SubscriptionMeta.id,
                SubscriptionMeta.init_quantity,
                SubscriptionMeta.subscription_id
            )
            .join(Subscription)
            .filter(Subscription.id.in_(subscription_ids))
        )
        return query.all()