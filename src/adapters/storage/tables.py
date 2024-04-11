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
    Column("account_id", String, ForeignKey("accounts.id"))
)

accounts_table = Table(
    "accounts",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("email", String),
)

bill_lines_table = Table(
    "bill_lines",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("summary", String),
    Column("region_name", String),
    Column("quantity", Integer),
    Column("subtotal", Integer),
    Column("total", Integer),
    Column("status", String),
    Column("discount_percent", Integer),
    Column("term_start_date", DateTime),
    Column("term_start_date", DateTime),
)

subscriptions_table = Table(
    "v4_subscriptions",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("resource_name", String),
    Column("resource_type", String),
    Column("related_ref", String),
    Column("category_id", String, ForeignKey("v4_categories.id"))
)

categories_table = Table(
    "v4_categories",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("summary", String),
)

products_table = Table(
    "v4_products",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("quantity_unit", String),
)

plans_table = Table(
    "plans",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("product_id", String, ForeignKey("v4_products.id"))
)

subscription_metas_table = Table(
    "subscription_metas",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("init_quantity", Integer),
    Column("subscription_id", String, ForeignKey("v4_subscriptions.id"))
)