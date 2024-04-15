import attrs


@attrs.define(slots=False, kw_only=True)
class Service:
    id: str
    name: str
