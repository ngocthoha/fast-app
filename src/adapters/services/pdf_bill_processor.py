from src.app.services.processors.base import BillProcessor, RenderType


class PDFBillProcessor(BillProcessor):
    template_directory: str = "cloud_server"
    _render_type = RenderType.PDF

    def generate_template(self, bill: dict, type: str = None, bill_lines: list = []):
        bill_id = bill.get("id")
        header_data = self._prepare_header_data(bill)
        bill_data = self._prepare_bill_data(bill_lines)
        payload = {
            "bill_id": bill_id,
            "type": type,
            "header_data": header_data,
            "bill_data": bill_data,
        }

        template = self._render_template(
            filename=f"{bill_id}.cloud_server.bill",
            payload=payload,
        )
        return template