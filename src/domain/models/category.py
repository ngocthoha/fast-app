import attrs


@attrs.define(slots=False, kw_only=True)
class Category:
    id: str
    summary: str