import attrs
from src.domain.models.product import Product


@attrs.define(slots=False, kw_only=True)
class Plan:
    id: str
    summary: str
    product: Product