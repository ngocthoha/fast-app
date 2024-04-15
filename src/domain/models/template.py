import attrs
from datetime import datetime


@attrs.define(slots=False, kw_only=True)
class Template:
    id: str
    name: str
    type: str
    start_date: datetime
    end_date: datetime