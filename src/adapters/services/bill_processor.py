from src.app.services.processors.base import BillProcessor, RenderTypeChoices


class CloudServerBillProcessor(BillProcessor):
    template_directory: str = "cloud_server"
    _render_type = RenderTypeChoices.PDF

    def __init__(self, template_id: str = None):
        super().__init__(template_id)

    def generate_template(self, bill: dict, type: str = None, bill_lines: list = []):
        bill_id = bill.get("id")
        header_data = self._prepare_header_data(bill)
        project_data, total_bill = self._prepare_project_data(bill, bill_lines)
        bill_data = self._prepare_bill_data(bill_lines)
        payload = {
            "bill_id": bill_id,
            "type": type,
            "header_data": header_data,
            "project_data": project_data,
            "total_bill": total_bill,
            "bill_data": bill_data,
        }

        template = self._render_template(
            filename=f"{bill_id}.cloud_server.bill",
            payload=payload,
        )
        return template
