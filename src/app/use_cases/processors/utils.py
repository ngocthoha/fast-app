from datetime import datetime


class RenderTemplateUtil:
    @classmethod
    def get_active_template_id(cls, templates, term_end_date):
        if not templates:
            return None

        mindate = datetime(1970, 1, 1)
        sorted_templates = sorted(
            templates, key=lambda x: x.start_date or mindate, reverse=True
        )
        if (
            sorted_templates[0].end_date is None
            or sorted_templates[0].end_date >= term_end_date
        ):
            return sorted_templates[0].id

        return None
