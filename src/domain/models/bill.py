from datetime import datetime
from .account import Account
import attrs


@attrs.define(slots=False, kw_only=True)
class Bill:
    id: str
    _created: datetime
    subtotal: int
    total: int
    term_start_date: datetime
    term_end_date: datetime
    account: Account
