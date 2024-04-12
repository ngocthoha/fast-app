from typing import List
import attrs
from src.domain.models.plan import Plan
from src.domain.models.category import Category


@attrs.define(slots=False, kw_only=True)
class Subscription:
    id: str
    region_name: str
    resource_name: str
    resource_type: str
    related_ref: str
    category: Category
    plan: Plan
