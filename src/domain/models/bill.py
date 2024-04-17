from datetime import datetime

import attrs

from .account import Account
from .service import Service


@attrs.define(slots=False, kw_only=True)
class Bill:
    id: str
    _created: datetime
    subtotal: int
    total: int
    term_start_date: datetime
    term_end_date: datetime
    account: Account
    service: Service
