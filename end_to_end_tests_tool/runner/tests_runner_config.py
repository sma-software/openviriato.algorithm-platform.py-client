class TestsRunnerConfig:
    __algorithm_interface_port_nr: int
    __connection_attempts_number: int
    __connection_retry_wait_seconds: float
    __config_file_on_relative_path: str
    __absolute_path_to_test_db: str
    __absolute_path_to_viriato: str
    __headless_executable: str
    __data_root_path_relative: str

    def __init__(self,
                 data_root_path_relative: str,
                 algorithm_interface_port_nr: int,
                 connection_attempts_number: int,
                 connection_retry_wait_seconds: float,
                 config_file_on_relative_path: str,
                 absolute_path_to_test_db: str,
                 absolute_path_to_viriato: str,
                 headless_executable: str):

        self.__data_root_path_relative = data_root_path_relative
        self.__algorithm_interface_port_nr = algorithm_interface_port_nr
        self.__connection_attempts_number = connection_attempts_number
        self.__connection_retry_wait_seconds = connection_retry_wait_seconds
        self.__config_file_on_relative_path = config_file_on_relative_path
        self.__absolute_path_to_test_db = absolute_path_to_test_db
        self.__absolute_path_to_viriato = absolute_path_to_viriato
        self.__headless_executable = headless_executable

    @property
    def data_root_path_relative(self) -> str:
        return self.__data_root_path_relative

    @property
    def algorithm_interface_port_nr(self) -> int:
        return self.__algorithm_interface_port_nr

    @property
    def connection_attempts_number(self) -> int:
        return self.__connection_attempts_number

    @property
    def connection_retry_wait_seconds(self) -> float:
        return self.__connection_retry_wait_seconds

    @property
    def config_file_on_relative_path(self) -> str:
        return self.__config_file_on_relative_path

    @property
    def absolute_path_to_test_db(self) -> str:
        return self.__absolute_path_to_test_db

    @property
    def absolute_path_to_viriato(self) -> str:
        return self.__absolute_path_to_viriato

    @property
    def headless_executable(self) -> str:
        return self.__headless_executable
