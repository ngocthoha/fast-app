from src.domain.models import Bill
from .tables import mapper_registry, bills_table


def setup_mapping():
    mapper_registry.map_imperatively(Bill, bills_table)
