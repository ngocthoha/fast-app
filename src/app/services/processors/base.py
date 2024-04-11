from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import Logger, getLogger
import subprocess
from jinja2 import Environment, FileSystemLoader
import os
import pdfkit

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
        self._jinja_env = Environment(
            loader=FileSystemLoader(f'{"/".join(__file__.split("/")[:-1])}/templates/{self.template_directory}/')
        )

    @property
    @abstractmethod
    def template_directory(self) -> str:
        """what template folder to use"""

    def _get_filepath(self, filename: str) -> str:
        return os.path.join(self.WORKDIR, filename)

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
        template = self._jinja_env.get_template(f"{template_name}.html.j2")
        css_path = f'{"/".join(__file__.split("/")[:-1])}/templates/static/styles.css'

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