from src.app.services.processors.base import BillProcessor, RenderType


class PDFBillProcessor(BillProcessor):
    template_directory: str = "cloud_server"
    _render_type = RenderType.PDF

    def generate_template(self, bill_id: str, type: str = None):
        payload = {}
        return self._render_template(
            "cloud_server.bill",
            payload,
        )