from sqlalchemy import Table, Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import registry
from sqlalchemy.sql import func

mapper_registry = registry()

bills_table = Table(
    "bills",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("subtotal", Integer),
    Column("total", Integer),
    Column("term_start_date", DateTime),
    Column("term_end_date", DateTime),
)
