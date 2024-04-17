from dataclasses import dataclass

import attrs

from src.app.use_cases.processors.utils import RenderTemplateUtil
from src.adapters.services import CloudServerBillProcessor
from src.app.services.unit_of_work import UnitOfWork
from src.utils.choices import TemplateTypeChoices


@dataclass
class RenderTemplateCommand:
    bill_id: str
    type: str


class RenderTemplateUseCase:

    BILL_PROCESSOR_MAPPING = {
        TemplateTypeChoices.CLOUD_SERVER: CloudServerBillProcessor
    }

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
                # add subscription metadata
                if str(bill_line["subscription_id"]) in meta_mapping:
                    bill_line["subscription"]["meta"] = meta_mapping.get(
                        bill_line["subscription_id"]
                    )

                # set has_same_related_ref to true if another bill line shares the same related_ref
                related_ref = bill_line.get("subscription").get("related_ref")
                if related_ref not in related_ref_mapping:
                    related_ref_mapping[related_ref] = [bill_line]
                    bill_line["has_same_related_ref"] = False
                else:
                    related_ref_mapping[related_ref].append(bill_line)
                    for b_line in related_ref_mapping[related_ref]:
                        if not b_line.get("has_same_related_ref", False):
                            b_line["has_same_related_ref"] = True

            with unit_of_work_custom:
                bill_type = bill.get("service", {}).get("name")
                term_start_date = bill.get("term_start_date").strftime("%Y-%m-%d")
                term_end_date = bill.get("term_end_date")
                templates = unit_of_work_custom.template_repository.find_templates(
                    bill_type, term_start_date
                )
                template_id = RenderTemplateUtil.get_active_template_id(
                    templates, term_end_date
                )

            bill_processor = self.BILL_PROCESSOR_MAPPING.get(bill_type)(
                template_id=template_id
            )

            return bill_processor.generate_template(
                bill=bill,
                type=command.type,
                bill_lines=bill_lines,
            )
