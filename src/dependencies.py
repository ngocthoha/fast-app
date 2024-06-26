import config

from .adapters.services import SQLAlchemyUnitOfWork
from .adapters.storage.engine import create_session_factory
from .adapters.storage.mapping import setup_mapping
from .app.services import CommandBus
from .app.use_cases import bill, template
from .app.use_cases.processors import render_tempate

# Session
setup_mapping()
session_factory = create_session_factory(uri=config.DB_URI)
session_factory_custom = create_session_factory(
    uri="postgresql://postgres:postgres@localhost:6868/postgres"
)

# Services
unit_of_work = SQLAlchemyUnitOfWork(session_factory)
unit_of_work_custom = SQLAlchemyUnitOfWork(session_factory_custom)

command_bus = CommandBus()

command_bus.register(bill.GetBillCommand, bill.GetBillUseCase(unit_of_work))
command_bus.register(
    render_tempate.RenderTemplateCommand,
    render_tempate.RenderTemplateUseCase(unit_of_work),
)
command_bus.register(
    template.CreateTemplateCommand,
    template.CreateTemplateUseCase(unit_of_work),  # noqa: E501
)


def get_unit_of_work():
    return unit_of_work


def get_command_bus():
    return command_bus
