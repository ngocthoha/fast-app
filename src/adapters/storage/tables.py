from sqlalchemy import Table, Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import registry
from sqlalchemy.sql import func

mapper_registry = registry()

bills_table = Table(
    "bills",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("_created", DateTime),
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
    Column("term_end_date", DateTime),
    Column("bill_id", String, ForeignKey("bills.id")),
    Column("subscription_id", String, ForeignKey("v4_subscriptions.id")),
)

subscriptions_table = Table(
    "v4_subscriptions",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("region_name", String),
    Column("resource_name", String),
    Column("resource_type", String),
    Column("related_ref", String),
    Column("category_id", String, ForeignKey("v4_categories.id")),
    Column("plan_id", String, ForeignKey("plans.id")),
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
    Column("summary", String),
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

services_table = Table(
    "services",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("name", String),
)


from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo = True)
meta = MetaData()

templates_table = Table(
   'templates', meta, 
   Column('id', String, primary_key = True), 
   Column('name', String), 
   Column('type', String),
   Column('start_date', DateTime),
   Column('end_date', DateTime),
)
# meta.create_all(engine)