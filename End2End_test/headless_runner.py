import os
import signal
import subprocess
import time
import requests
from AlgorithmInterface.AlgorithmInterface import AlgorithmicPlatformInterface


class ViriatoHeadlessRunnerConfig:
    config_file_with_relative_path: str
    test_db_with_absolute_path: str
    absolute_path_to_viriato: str

    def __init__(
            self,
            config_file_with_relative_path: str,
            test_db_with_absolute_path: str,
            absolute_path_to_viriato: str):
        self.config_file_with_relative_path = config_file_with_relative_path
        self.test_db_with_absolute_path = test_db_with_absolute_path
        self.absolute_path_to_viriato = absolute_path_to_viriato


class ViriatoHeadlessRunner:
    __subprocess_running_headless: subprocess.Popen = None
    __remaining_connection_attempts = 5
    __connection_wait_time = 4
    __headless_runner_config: ViriatoHeadlessRunnerConfig
    __headless_exe_name = "SMA.Viriato.AlgorithmPlatform.Headless.exe"

    def __init__(self, headless_runner_config: ViriatoHeadlessRunnerConfig):
        self.__headless_runner_config = headless_runner_config
        self.__start_headless_viriato()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__subprocess_running_headless is not None:
            self.safely_interrupt_headless()

    def __start_headless_viriato(self):
        headless_command_line_call = (
                self.__headless_exe_name +
                ' ' +
                self.__headless_runner_config.test_db_with_absolute_path +
                ' ' +
                self.__headless_runner_config.config_file_with_relative_path)
        current_working_dir = os.getcwd()
        try:
            os.chdir(self.__headless_runner_config.absolute_path_to_viriato)
            self.__subprocess_running_headless = subprocess.Popen(headless_command_line_call, shell=True)
        finally:
            os.chdir(current_working_dir)

    def check_and_wait_for_headless_to_be_ready(self, algorithm_interface: AlgorithmicPlatformInterface):

        while self.__remaining_connection_attempts > 1:
            time.sleep(self.__connection_wait_time)
            try:
                algorithm_interface.notify_user('this_is_just', 'to_test_if_there_is_a_connection')
                break
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                print("Warning *** \n No connection to headless, trying once more in {0} seconds"
                      .format(self.__connection_wait_time))
                self.__remaining_connection_attempts -= 1

        if self.__remaining_connection_attempts < 2:
            time.sleep(self.__connection_wait_time)
            print("Warning *** \n Could not connect to headless, final attempt \n")
            algorithm_interface.notify_user('this_is_just', 'to_test_if_there_is_a_connection')

        print("connected to headless on URL\n{0}\n".format(algorithm_interface.base_url))

    def check_if_headless_is_still_running(self) -> bool:
        process_is_still_running = self.__subprocess_running_headless.poll() is None
        return process_is_still_running

    def safely_interrupt_headless(self):
        if self.check_if_headless_is_still_running():
            try:
                self.__subprocess_running_headless.send_signal(signal.CTRL_C_EVENT)
                print('shutting down Headless')
                while self.check_if_headless_is_still_running():
                    print('shutdown in progress')
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
