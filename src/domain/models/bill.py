from datetime import datetime

import attrs


@attrs.define(slots=False, kw_only=True)
class Bill:
    id: str
    subtotal: int
    total: int
    term_start_date: datetime
    term_end_date: datetime
