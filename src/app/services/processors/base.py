from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from logging import Logger, getLogger
from jinja2 import Environment, FileSystemLoader
import os
import pdfkit
from src.utils.choices import PlanSummaryChoices
from src.utils.billing_date_time import parse_current_time

LOG: Logger = getLogger(__name__)


class BillType:
    CLOUD_SERVER = "cloud_server"
    CLOUD_DATABASE = "dbaas"


class RenderType:
    PDF = "PDF"
    CSV = "CSV"


class BillStatusChoices:
    PAID = "paid"
    UNPAID = "unpaid"


RESOURCE_SUMMARY_MAPPING = {
    PlanSummaryChoices.CDN_DATA_TRANSFER: "Data Transfer",
    PlanSummaryChoices.S3_DATA_TRANSFER: "Data Transfer",
    PlanSummaryChoices.S3_DATA_TRANSFER_TRIAL: "Data Transfer",
    PlanSummaryChoices.S3_STORAGE: "Storage",
    PlanSummaryChoices.S3_STORAGE_TRIAL: "Storage",
    PlanSummaryChoices.S3_REQUEST: "Request",
    PlanSummaryChoices.S3_STANDARD: "Standard",
}


class BillProcessor(ABC):
    WORKDIR: str = "bills"
    _jinja_env = None
    _render_type = None

    @dataclass
    class WKHtmlToPDFConfig:
        page_size: str = "A4"
        minimum_font_size: str = "5"

    def __init__(self, template_id: str = None):
        self.template_id = template_id
        template_path = f'src/templates/{self.template_directory}/'
        if template_id is not None:
            template_path = f"{template_path}{template_id}/"
        self._jinja_env = Environment(
            loader=FileSystemLoader(template_path)
        )
        # self._jinja_env = Environment(
        #     loader=FileSystemLoader('D:\\BizflyCloud\\fast-app\\src\\app\\services\\processors\\templates\\cloud_server\\')
        # )
        self._jinja_env.globals.update(
            {
                "get_group_summary": BillProcessor.get_group_summary,
                "get_group_start_date": BillProcessor.get_group_start_date,
                "get_group_end_date": BillProcessor.get_group_end_date,
            }
        )
        self._jinja_env.filters.update(
            {
                "format_currency": BillProcessor.format_currency,
            }
        )

    @property
    @abstractmethod
    def template_directory(self) -> str:
        """what template folder to use"""

    def _get_filepath(self, filename: str) -> str:
        return os.path.join(self.WORKDIR, filename)

    @classmethod
    def format_currency(self, number):
        import locale

        locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
        return locale.format_string("%.2f", number, grouping=True)

    def _get_active_template(self, bill_type):
        pass

    @classmethod
    def get_group_start_date(cls, groups):
        def extract_date(date_str):
            return datetime.strptime(date_str, "%H:%M %d/%m/%Y")

        sorted_groups = sorted(
            groups,
            key=lambda x: extract_date(x["term_start_date"]),
        )
        return datetime.strptime(sorted_groups[0]["term_start_date"], "%H:%M %d/%m/%Y").strftime("%d/%m/%Y")

    @classmethod
    def get_group_end_date(cls, groups):
        def extract_date(date_str):
            return datetime.strptime(date_str, "%H:%M %d/%m/%Y")

        sorted_groups = sorted(
            groups,
            key=lambda x: extract_date(x["term_end_date"]),
        )
        return datetime.strptime(sorted_groups[-1]["term_end_date"], "%H:%M %d/%m/%Y").strftime("%d/%m/%Y")

    @classmethod
    def get_group_summary(cls, groups):
        for group in groups:
            if group.get("summary") and ("RAM" in group.get("summary") or "CPU" in group.get("summary")):
                return group.get("summary").split()[0]
        return ""

    def _get_resource_summary(self, subscription: str):
        if subscription.get("plan", {}).get("summary") in RESOURCE_SUMMARY_MAPPING:
            return RESOURCE_SUMMARY_MAPPING.get(subscription.get("plan", {}).get("summary"))

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
            "template_id": self.template_id,
        }
        return [header_data]

    def _get_total_bill(self, bill_lines: list):
        unpaid_total = 0
        paid_total = 0
        subtotal = 0
        subtotal_discount = 0
        for bill_line in bill_lines:
            paid_total += (
                bill_line.get("total")
                if bill_line.get("status") == BillStatusChoices.PAID
                else 0
            )
            unpaid_total += (
                bill_line.get("total")
                if bill_line.get("status") == BillStatusChoices.UNPAID
                else 0
            )
            subtotal += bill_line.get("subtotal")
            discount_total = (
                int(bill_line.get("subtotal"))
                * bill_line.get("discount_percent", {})
                / 100
            )
            discount_after = int(bill_line.get("subtotal")) - discount_total
            subtotal_discount += discount_after

        paid_total = f"{paid_total:,}".replace(",", ".")
        unpaid_total = BillProcessor.format_currency(unpaid_total)
        subtotal = f"{subtotal:,}".replace(",", ".")
        subtotal_discount = f"{int(subtotal_discount):,}".replace(",", ".")

        total_bill = [
            {
                "subtotal": subtotal,
                "unpaid_total": unpaid_total,
                "paid_total": paid_total,
                "subtotal_discount": subtotal_discount,
            }
        ]

        return total_bill, unpaid_total

    def _prepare_project_data(self, bill: dict, bill_lines: list):
        total_bill, unpaid_total = self._get_total_bill(bill_lines)
        project_data = []
        project_data.append(
            {
                "project_name": bill.get("account", {}).get("email"),
                "unpaid_total": unpaid_total
            }
        )

        return project_data, total_bill

    def _prepare_bill_data(self, bill_lines: list):
        """
        Prepares data for rendering template
        """
        list_bill_line = []
        subscription_mapping = {}
        for bill_line in bill_lines:
            if bill_line.get("subscription_id") not in subscription_mapping:
                bill_line["unpaid_total"] = bill_line["total"] if bill_line["status"] == BillStatusChoices.UNPAID else 0
                bill_line["paid_total"] = bill_line["total"] if bill_line["status"] == BillStatusChoices.PAID else 0
                subscription_mapping[bill_line.get("subscription_id")] = bill_line
            else:
                current_bill_line = subscription_mapping.get(bill_line.get("subscription_id"))
                current_bill_line["subtotal"] += bill_line["subtotal"]
                if bill_line["status"] == BillStatusChoices.UNPAID:
                    current_bill_line["unpaid_total"] += bill_line["total"]
                if bill_line["status"] == BillStatusChoices.PAID:
                    current_bill_line["paid_total"] += bill_line["total"]

                subscription_mapping[bill_line.get("subscription_id")] = current_bill_line

        for bill_line in subscription_mapping.values():
            list_bill_line.append(
                {
                    "id": bill_line.get("id"),
                    "summary": bill_line.get("summary"),
                    "project_name": bill_line.get("bill", {}).get("account", {}).get("email"),
                    "region_name": bill_line.get("subscription", {}).get("region_name"),
                    "resource_summary": self._get_resource_summary(bill_line.get("subscription")),
                    "related_ref": bill_line.get("subscription", {}).get("related_ref"),
                    "term_start_date": bill_line.get("term_start_date").strftime("%H:%M %d/%m/%Y"),
                    "term_end_date": bill_line.get("term_end_date").strftime("%H:%M %d/%m/%Y"),
                    "quantity": int(bill_line.get("quantity")),
                    "subtotal": bill_line.get("subtotal"),
                    "discount_percent": bill_line.get("discount_percent"),
                    "discount_total": bill_line.get("subtotal") - (bill_line.get("paid_total") + bill_line.get("unpaid_total")),
                    "final_total": bill_line.get("paid_total") + bill_line.get("unpaid_total"),
                    "paid_total": bill_line.get("paid_total"),
                    "unpaid_total": bill_line.get("unpaid_total"),
                    "has_same_related_ref": bill_line.get("has_same_related_ref"),
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
        in_filepath = f"{filepath}.html"
        out_filepath = f"{filepath}.pdf"
        # in_filepath = "D:\\BizflyCloud\\fast-app\\bills\\bd416a7e-1bec-45be-955f-b101c3375e12.cloud_server.bill.html"
        # out_filepath = "D:\\BizflyCloud\\fast-app\\bills\\bd416a7e-1bec-45be-955f-b101c3375e12.cloud_server.bill.pdf"
        template = self._jinja_env.get_template(f"{template_name}.html.j2")
        css_path = "src/templates/static/styles.css"
        # css_path = "D:\\BizflyCloud\\fast-app\\src\\app\\services\\processors\\templates\\static\\styles.css"

        rendered_template = template.render(
            css_path=css_path,
            **payload,
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