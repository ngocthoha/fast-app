from datetime import datetime

import attrs

from domain.models.bill import Bill


@attrs.define(slots=False, kw_only=True)
class BillLine:
    id: str
    summary: str
    region_name: str
    quantity: int
    subtotal: int
    total: int
    status: str
    discount_percent: int
    term_start_date: datetime
    term_end_date: datetime
    bill: Bill
