class SetupToolsArguments:
    __release_package_requirements_on_relative_path: str
    __version: str
    __project_root_directory: str
    __output_directory: str

    def __init__(self,
                 release_package_requirements_on_relative_path: str,
                 py_client_version_number: str,
                 project_root_directory: str,
                 output_directory: str):

        self.__release_package_requirements_on_relative_path = release_package_requirements_on_relative_path
        self.__py_client_version = py_client_version_number
        self.__project_root_directory = project_root_directory
        self.__output_directory = output_directory

    @property
    def release_package_requirements_on_relative_path(self) -> str:
        return self.__release_package_requirements_on_relative_path

    @property
    def py_client_build_number(self) -> str:
        return self.__version

    @property
    def project_root_directory(self) -> str:
        return self.__project_root_directory

    @property
    def output_directory(self) -> str:
        return self.__output_directory
