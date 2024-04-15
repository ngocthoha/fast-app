from dataclasses import dataclass
import json

import attrs
from src.app.services.unit_of_work import UnitOfWork
from src.adapters.services import CloudServerBillProcessor
from src.dependencies import unit_of_work_custom


@dataclass
class RenderTemplateCommand:
    bill_id: str
    type: str


class RenderTemplateUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def execute(self, command: RenderTemplateCommand):
        with self._uow:
            bill = self._uow.bill_repository.find_by_id(command.bill_id)
            bill = attrs.asdict(bill)

            bill_lines = self._uow.bill_line_repository.find_bill_lines_by_bill_id(
                command.bill_id
            )
            bill_lines = [attrs.asdict(bill_line) for bill_line in bill_lines]

            subscription_ids = [bill_line.get("subscription").get("id") for bill_line in bill_lines]
            metas = self._uow.subscription_meta_repository.find_by_subscription_ids(subscription_ids)
            metas = [meta._asdict() for meta in metas]

            meta_mapping = {str(meta["subscription_id"]): meta for meta in metas}
            related_ref_mapping = {}

            for bill_line in bill_lines:
                if str(bill_line["subscription_id"]) in meta_mapping:
                    bill_line["subscription"]["meta"] = meta_mapping.get(bill_line["subscription_id"])

                related_ref = bill_line.get("subscription").get("related_ref")
                if related_ref not in related_ref_mapping:
                    related_ref_mapping[related_ref] = False
                else:
                    related_ref_mapping[related_ref] = True

            for bill_line in bill_lines:
                related_ref = bill_line.get("subscription").get("related_ref")
                if related_ref_mapping[related_ref]:
                    bill_line["has_same_related_ref"] = True
                else:
                    bill_line["has_same_related_ref"] = False

            with unit_of_work_custom:
                bill_type = bill.get("service", {}).get("name")
                unit_of_work_custom.template_repository.find_active_templates(bill_type)
            
            cloud_server_bill_processor = CloudServerBillProcessor()
            return cloud_server_bill_processor.generate_template(
                bill=bill,
                type=command.type,
                bill_lines=bill_lines,
            )