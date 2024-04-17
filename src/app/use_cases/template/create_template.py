import os
import shutil
import zipfile
from dataclasses import dataclass
from logging import Logger, getLogger

from fastapi import File

from src.app.services.unit_of_work import UnitOfWork
from src.domain.models.template import Template

LOG: Logger = getLogger(__name__)


CHUNK_SIZE = 1024 * 1024


@dataclass
class CreateTemplateCommand:
    file: File
    type: str
    name: str
    start_date: str
    end_date: str


@dataclass
class CreateTemplateResponse:
    id: str
    type: str
    name: str
    start_date: str
    end_date: str


class CreateTemplateUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def execute(self, command: CreateTemplateCommand):
        from src.dependencies import unit_of_work_custom

        with unit_of_work_custom:
            template_id = unit_of_work_custom.template_repository.generate_id()
            template = Template(
                id=template_id,
                type=command.type,
                name=command.name,
                start_date=command.start_date,
                end_date=command.end_date,
            )
            unit_of_work_custom.template_repository.save(template)
            unit_of_work_custom.commit()

            try:
                file = command.file
                type = command.type
                directory = f"src/templates/{type}/{template.id}"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # save the zip file
                file_location = f"{directory}/{os.path.basename(file.filename)}"
                with open(file_location, "wb") as f:
                    while chunk := file.file.read(CHUNK_SIZE):
                        f.write(chunk)

                # extract the zip file
                with zipfile.ZipFile(file_location, "r") as zip_ref:
                    zip_ref.extractall(directory)

                def move_files_to_main(source, destination):
                    files = os.listdir(source)
                    for file in files:
                        file_name = os.path.join(source, file)
                        shutil.move(file_name, destination)

                # move the files to the main directory
                original_filename = f"{directory}/{file.filename}"
                if ".zip" in file.filename:
                    original_filename = original_filename.rsplit(".", 1)[0]

                move_files_to_main(original_filename, directory)
            except Exception as e:
                LOG.warning("Error: %s", e)
            finally:
                os.remove(file_location)
                os.rmdir(original_filename)

            return CreateTemplateResponse(
                id=template.id,
                type=template.type,
                name=template.name,
                start_date=template.start_date,
                end_date=template.end_date,
            )
