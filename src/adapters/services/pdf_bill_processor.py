from src.app.services.processors.base import BillProcessor, RenderType


class PDFBillProcessor(BillProcessor):
    template_directory: str = "cloud_server"
    _render_type = RenderType.PDF

    def generate_template(self, bill_id: str, type: str = None, bill_data: list = []):
        payload = {
            "bill_id": bill_id,
            "type": type,
            "bill_data": bill_data,
        }
        template = self._render_template(
            filename=f"{bill_id}.cloud_server.bill",
            payload=payload,
        )
        return template