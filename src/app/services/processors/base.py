from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader
import os


class RenderType:
    PDF = "PDF"
    CSV = "CSV"


class BillProcessor(ABC):

    _jinja_env = None
    _render_type = None

    def __init__(self):
        self._jinja_env = Environment(
            loader=FileSystemLoader(f'{"/".join(__file__.split("/")[:-1])}/templates/{self.template_directory}/')
        )

    @property
    @abstractmethod
    def template_directory(self) -> str:
        """what template folder to use"""

    def _get_filepath(self, filename: str) -> str:
        return os.path.join(self.WORKDIR, self.report_id, filename)

    def _render_template(self, filename: str, payload: dict, template_name: str = "bill"):
        if self._render_type == RenderType.PDF:
            return self._render_pdf_template(filename, payload, template_name)


    @abstractmethod
    def _render_pdf_template(self, filename: str, payload: dict, template_name: str = "bill"):
        """
        Renders the jinja template in the configured template directory
        """
        filepath = self._get_filepath(filename)
        in_filepath = f"{filepath}.html"
        out_filepath = f"{filepath}.pdf"

        template = self._jinja_env.get_template(f"{template_name}.html.j2")
        rendered_template = template.render(**payload)
        with open(in_filepath, "w") as f:
            f.write(rendered_template)