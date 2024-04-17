import attrs


@attrs.define(slots=False, kw_only=True)
class Product:
    id: str
    summary: str
    quantity_unit: str
