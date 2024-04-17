from sqlalchemy.orm import relationship

from src.domain.models import (
    Account,
    Bill,
    BillLine,
    Category,
    Plan,
    Product,
    Service,
    Subscription,
    SubscriptionMeta,
    Template,
)

from .tables import (
    accounts_table,
    bill_lines_table,
    bills_table,
    categories_table,
    mapper_registry,
    plans_table,
    products_table,
    services_table,
    subscription_metas_table,
    subscriptions_table,
    templates_table,
)


def setup_mapping():
    mapper_registry.map_imperatively(Account, accounts_table)
    mapper_registry.map_imperatively(
        Bill,
        bills_table,
        properties={
            "account": relationship(Account),
            "service": relationship(Service),
        },
    )
    mapper_registry.map_imperatively(
        BillLine,
        bill_lines_table,
        properties={
            "bill": relationship(Bill),
            "subscription": relationship(Subscription),
        },
    )
    mapper_registry.map_imperatively(
        Subscription,
        subscriptions_table,
        properties={
            "category": relationship(Category),
            "plan": relationship(Plan),
        },
    )
    mapper_registry.map_imperatively(
        SubscriptionMeta,
        subscription_metas_table,
        properties={
            "subscription": relationship(Subscription),
        },
    )
    mapper_registry.map_imperatively(
        Plan,
        plans_table,
        properties={
            "product": relationship(Product),
        },
    )
    mapper_registry.map_imperatively(Product, products_table)
    mapper_registry.map_imperatively(Category, categories_table)
    mapper_registry.map_imperatively(Service, services_table)
    mapper_registry.map_imperatively(Template, templates_table)
