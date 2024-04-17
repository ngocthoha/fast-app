from dataclasses import dataclass

import attrs

from src.adapters.services import CloudServerBillProcessor
from src.app.services.unit_of_work import UnitOfWork
from src.utils.choices import TemplateChoices

BILL_PROCESSOR_MAPPING = {TemplateChoices.CLOUD_SERVER: CloudServerBillProcessor}


@dataclass
class RenderTemplateCommand:
    bill_id: str
    type: str


class RenderTemplateUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def execute(self, command: RenderTemplateCommand):
        from src.dependencies import unit_of_work_custom

        with self._uow:
            bill = self._uow.bill_repository.find_by_id(command.bill_id)
            bill = attrs.asdict(bill)

            bill_lines = self._uow.bill_line_repository.find_bill_lines_by_bill_id(
                command.bill_id
            )
            bill_lines = [attrs.asdict(bill_line) for bill_line in bill_lines]

            subscription_ids = [
                bill_line.get("subscription").get("id") for bill_line in bill_lines
            ]
            metas = self._uow.subscription_meta_repository.find_by_subscription_ids(
                subscription_ids
            )
            metas = [meta._asdict() for meta in metas]

            meta_mapping = {str(meta["subscription_id"]): meta for meta in metas}
            related_ref_mapping = {}

            for bill_line in bill_lines:
                if str(bill_line["subscription_id"]) in meta_mapping:
                    bill_line["subscription"]["meta"] = meta_mapping.get(
                        bill_line["subscription_id"]
                    )

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
                from datetime import datetime

                bill_type = bill.get("service", {}).get("name")
                term_start_date = bill.get("term_start_date").strftime("%Y-%m-%d")
                term_end_date = bill.get("term_end_date")
                templates = (
                    unit_of_work_custom.template_repository.find_active_templates(
                        bill_type, term_start_date
                    )
                )
                template_id = None
                if templates:
                    mindate = datetime(1970, 1, 1)
                    sorted_templates = sorted(
                        templates, key=lambda x: x.start_date or mindate, reverse=True
                    )
                    if (
                        sorted_templates[0].end_date is None
                        or sorted_templates[0].end_date >= term_end_date
                    ):
                        template_id = sorted_templates[0].id

            bill_processor = BILL_PROCESSOR_MAPPING.get(bill_type)
            if bill_processor is None:
                bill_processor = CloudServerBillProcessor

            bp = bill_processor(template_id=template_id)
            return bp.generate_template(
                bill=bill,
                type=command.type,
                bill_lines=bill_lines,
            )
