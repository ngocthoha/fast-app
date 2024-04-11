from datetime import datetime


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
