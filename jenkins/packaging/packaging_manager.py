import os
from setuptools import setup
from typing import TypeVar, List
from jenkins.packaging.packaging_arguments import SetupToolsArguments

SELF = TypeVar('SELF', bound="PackagingManager")

PACKAGE_BASENAME: str = "algorithmplatform"
PACKAGE_OUTPUT_SUFFIX: str = "py3-none-any"


class PackagingManager:

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
    def __create_version_id_from_build_number(py_client_build_number: str):
        return

    @staticmethod
    def __rename_wheel_after_packaging(output_directory: str, py_client_version: str) -> bool:
        packaging_file_name = os.path.join(
            output_directory, "{0}-{1}-{2}.whl".format(
                PACKAGE_BASENAME,
                py_client_version,
                PACKAGE_OUTPUT_SUFFIX))

        desired_file_name = os.path.join(
            output_directory,
            "{0}-{1}.whl".format(PACKAGE_BASENAME, py_client_version))

        os.rename(packaging_file_name, desired_file_name)

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
                'py_client.aidm', 'py_client.Conversion', 'py_client.Communication', 'py_client.algorithm_interface'],
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
			
		self.__rename_wheel_after_packaging(
            os.path.join(current_working_directory, setup_tools_arguments.output_directory),
            setup_tools_arguments.py_client_version)
		return True
