from domain.models.category import Category


class Subscription:
    id: str
    resource_name: str
    resource_type: str
    related_ref: str
    category: Category
