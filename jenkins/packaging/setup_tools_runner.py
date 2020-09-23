import os
from typing import TypeVar, List

from setuptools import setup

import py_client.aidm
import py_client.algorithm_interface
import py_client.communication
import py_client.conversion
from jenkins.packaging.setup_tools_arguments import SetupToolsArguments

SELF = TypeVar('SELF', bound="PackagingManager")

PACKAGE_BASENAME: str = "algorithmplatform"
PACKAGE_OUTPUT_SUFFIX: str = "py3-none-any"


class SetupToolsRunner:

    @staticmethod
    def __switch_working_directory_for_packaging(packaging_root_directory: str):
        os.chdir(packaging_root_directory)

    @staticmethod
    def __start_packaging_as_instructed(packaging_parameters: dict):
        setup(**packaging_parameters)

    @staticmethod
    def __switch_working_directory_back_to_previous_one(current_working_directory: str):
        os.chdir(current_working_directory)

    @staticmethod
    def __assemble_arguments_dictionary_for_setup(setup_tools_arguments: SetupToolsArguments) -> dict:
        def read_required_packages_from_requirements_file_name(release_package_requirements_filename: str) -> List[str]:
            with open(release_package_requirements_filename, 'r') as f:
                return f.read().splitlines()

        return dict(
            install_requires=read_required_packages_from_requirements_file_name(
                setup_tools_arguments.release_package_requirements_on_relative_path),
            name=PACKAGE_BASENAME,
            version=setup_tools_arguments.py_client_version,
            packages=[
                py_client.aidm.__name__,
                py_client.conversion.__name__,
                py_client.communication.__name__,
                py_client.algorithm_interface.__name__],
            url='https://www.sma-partner.com',
            license='',
            author='',
            author_email='',
            description='',
            script_args=["bdist_wheel", "-d", os.path.abspath(setup_tools_arguments.output_directory)])

    def make_package(self, setup_tools_arguments: SetupToolsArguments):
        absolute_project_root_dir = os.path.abspath(setup_tools_arguments.project_root_directory)
        current_working_directory = os.getcwd()
        setup_tools_arguments_dictionary = self.__assemble_arguments_dictionary_for_setup(
            setup_tools_arguments)

        self.__switch_working_directory_for_packaging(absolute_project_root_dir)
        try:
            self.__start_packaging_as_instructed(setup_tools_arguments_dictionary)
        finally:
            self.__switch_working_directory_back_to_previous_one(current_working_directory)

        return True
