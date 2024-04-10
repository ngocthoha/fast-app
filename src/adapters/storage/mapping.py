from src.domain.models import Bill, Account
from .tables import mapper_registry, bills_table, accounts_table
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
