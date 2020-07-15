import os
from setuptools import setup
from typing import TypeVar, Optional

SELF = TypeVar('SELF', bound="PackagingManager")


class PackagingManager:
    __packaging_parameters: dict
    __packaging_root_directory: str
    __current_directory: Optional[str] = None

    def __init__(self, packaging_parameters: dict, packaging_root_directory: str):
        self.__packaging_parameters = packaging_parameters
        self.__packaging_root_directory = packaging_root_directory

    @property
    def packaging_root_directory(self) -> str:
        return self.__packaging_root_directory

    @property
    def packaging_parameters(self) -> dict:
        return self.__packaging_parameters

    def __switch_working_directory_for_packaging(self):
        self.__current_directory = os.getcwd()
        os.chdir(self.packaging_root_directory)

    def __start_packaging_as_instructed(self):
        setup(**self.packaging_parameters)

    def __switch_working_directory_back_to_previous_one(self):
        os.chdir(self.__current_directory)

    @classmethod
    def create_and_start_packaging_manager(cls, setup_instructions: dict, root_directory: str) -> SELF:
        packaging_manager = PackagingManager(setup_instructions, root_directory)
        packaging_manager.__switch_working_directory_for_packaging()
        try:
            packaging_manager.__start_packaging_as_instructed()
        finally:
            packaging_manager.__switch_working_directory_back_to_previous_one()
        return packaging_manager
