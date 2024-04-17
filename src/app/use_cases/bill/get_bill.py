from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import attrs

from src.app.services import UnitOfWork
from src.domain.models import Account


@dataclass
class GetBillCommand:
    bill_id: str


@dataclass
class GetBillResponse:
    id: str
    subtotal: int
    total: int
    term_start_date: datetime
    term_end_date: datetime
    account: Account


class GetBillUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def execute(self, command: GetBillCommand) -> GetBillResponse:
        with self._uow:
            bill = self._uow.bill_repository.find_by_id(command.bill_id)
            if bill is None or bill.id != command.bill_id:
                raise ValueError("Invalid bill_id")
            bill_dict = attrs.asdict(bill)
            return GetBillResponse(**bill_dict)
