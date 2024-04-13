from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from logging import Logger, getLogger
import subprocess
from jinja2 import Environment, FileSystemLoader
import os
import pdfkit
import dateutil.parser
from src.utils.billing_date_time import parse_current_time

LOG: Logger = getLogger(__name__)

class RenderType:
    PDF = "PDF"
    CSV = "CSV"


class BillProcessor(ABC):
    WORKDIR: str = "bills"
    _jinja_env = None
    _render_type = None

    @dataclass
    class WKHtmlToPDFConfig:
        page_size: str = "A4"
        minimum_font_size: str = "5"

    def __init__(self):
        # self._jinja_env = Environment(
        #     loader=FileSystemLoader(f'{"/".join(__file__.split("/")[:-1])}/templates/{self.template_directory}/')
        # )
        self._jinja_env = Environment(
            loader=FileSystemLoader('D:\\BizflyCloud\\fast-app\\src\\app\\services\\processors\\templates\\cloud_server\\')
        )

    @property
    @abstractmethod
    def template_directory(self) -> str:
        """what template folder to use"""

    def _get_filepath(self, filename: str) -> str:
        return os.path.join(self.WORKDIR, filename)

    def _parse_resource_name(self, subscription: str):
        product = subscription.get("plan", {}).get("product").get("summary")
        resource_name = subscription.get("resource_name")
        category = subscription.get("category", {}).get("summary")
        quantity = int(subscription.get("meta", {}).get("init_quantity"))
        quantity_unit = (
            subscription.get("plan", {}).get("product").get("quantity_unit").upper()
        )
        return f"{product} {category}: {resource_name} {quantity}{quantity_unit}"

    def _prepare_header_data(self, bill: dict):
        _created = bill.get("_created", {})
        header_data = {
            "account": bill.get("account").get("email"),
            "created_date": _created,
            "start_date": bill.get("term_start_date"),
            "end_date": bill.get("term_end_date"),
        }
        return [header_data]

    def _prepare_project_data(self, bill: dict):
        project_data = []
        project_data.append(
            {
                "index": 1,
                "project_name": bill.get("account", {}).get("email"),
                "total_bill_unpaid": bill.get("total")
            }
        )
        total_bill = 0
        for project in project_data:
            total_bill += project.get("total_bill_unpaid")

        return project_data, total_bill

    def _prepare_bill_data(self, bill_lines: list):
        """
        Prepares data for rendering template
        """
        list_bill_line = []
        for bill_line in bill_lines:
            list_bill_line.append(
                {
                    "project_name": bill_line.get("bill", {}).get("account", {}).get("email"),
                    "region_name": bill_line.get("subscription", {}).get("region_name"),
                    "resource_name": self._parse_resource_name(bill_line.get("subscription")),
                    "term_start_date": bill_line.get("term_start_date"),
                    "term_end_date": bill_line.get("term_end_date"),
                    "quantity": bill_line.get("quantity"),
                    "subtotal": bill_line.get("subtotal"),
                    "discount_percent": bill_line.get("discount_percent"),
                    "total_discount": bill_line.get("subtotal") - bill_line.get("total"),
                    "paid_total": bill_line.get("total"),
                    "unpaid_total": bill_line.get("total")
                }
            )
        
        return list_bill_line

    def _render_template(self, filename: str, payload: dict, template_name: str = "bill"):
        """
        Renders the appropriate template
        """
        if self._render_type == RenderType.PDF:
            return self._render_pdf_template(filename, payload, template_name)

    def _render_pdf_template(
            self,
            filename: str,
            payload: dict,
            template_name: str = "bill", 
            wkhtmltox_config: WKHtmlToPDFConfig = None
        ):
        """
        Renders the jinja template in the configured template directory
        """
        if wkhtmltox_config is None:
            wkhtmltox_config = self.WKHtmlToPDFConfig()

        filepath = self._get_filepath(filename)
        # in_filepath = f"{filepath}.html"
        # out_filepath = f"{filepath}.pdf"
        in_filepath = "D:\\BizflyCloud\\fast-app\\bills\\bd416a7e-1bec-45be-955f-b101c3375e12.cloud_server.bill.html"
        out_filepath = "D:\\BizflyCloud\\fast-app\\bills\\bd416a7e-1bec-45be-955f-b101c3375e12.cloud_server.bill.pdf"
        template = self._jinja_env.get_template(f"{template_name}.html.j2")
        # css_path = f'{"/".join(__file__.split("/")[:-1])}/templates/static/styles.css'
        css_path = "D:\\BizflyCloud\\fast-app\\src\\app\\services\\processors\\templates\\static\\styles.css"

        rendered_template = template.render(
            css_path=css_path,
            **payload
        )
        with open(in_filepath, "w") as f:
            f.write(rendered_template)

        options = {
            'page-size': wkhtmltox_config.page_size or "A4",
            'minimum-font-size': wkhtmltox_config.minimum_font_size or "5",
            "enable-local-file-access": ""
        }

        try:
            pdfkit.from_file(
                in_filepath, 
                out_filepath,
                css=css_path,
                options=options
            )
        except Exception as e:
            LOG.warning("WKHTMLTOPDF Error: %s", e)
        finally:
            os.remove(in_filepath)

        return out_filepath