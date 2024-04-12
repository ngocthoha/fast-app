from src.domain.models import Bill, Account, BillLine, Subscription, SubscriptionMeta, Plan, Product, Category
from .tables import mapper_registry, bills_table, accounts_table, bill_lines_table, subscriptions_table, subscription_metas_table, plans_table, products_table, categories_table
from sqlalchemy.orm import relationship


def setup_mapping():
    mapper_registry.map_imperatively(Account, accounts_table)
    mapper_registry.map_imperatively(
        Bill,
        bills_table,
        properties={
            "account": relationship(Account),
        }
    )
    mapper_registry.map_imperatively(
        BillLine,
        bill_lines_table,
        properties={
            "bill": relationship(Bill),
            "subscription": relationship(Subscription),
        }
    )
    mapper_registry.map_imperatively(
        Subscription, 
        subscriptions_table,
        properties={
            "category": relationship(Category),
            "plan": relationship(Plan),
        }
    )
    mapper_registry.map_imperatively(
        SubscriptionMeta, 
        subscription_metas_table,
        properties={
            "subscription": relationship(Subscription),
        }
    )
    mapper_registry.map_imperatively(
        Plan, 
        plans_table,
        properties={
            "product": relationship(Product),
        }
    )
    mapper_registry.map_imperatively(Product, products_table)
    mapper_registry.map_imperatively(Category, categories_table)