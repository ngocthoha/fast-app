import attrs


@attrs.define(slots=False, kw_only=True)
class Account:
    id: str
    name: str
    email: str
