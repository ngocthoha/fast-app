from datetime import datetime

import attrs


@attrs.define(slots=False, kw_only=True)
class Template:
    id: str
    name: str
    type: str
    start_date: datetime
    end_date: datetime
