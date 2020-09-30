import os
import signal
import subprocess
import time
from typing import Optional

import requests

from End_to_end_tests_tool.runner.tests_runner_config import TestsRunnerConfig
from py_client.algorithm_interface.algorithm_interface_factory import AlgorithmInterface
from py_client.communication.response_processing import AlgorithmPlatformError


class ViriatoHeadlessRunner:
    __subprocess_running_headless: Optional[subprocess.Popen] = None
    __remaining_connection_attempts: int
    headless_runner_config: TestsRunnerConfig

    def __init__(self, actual_headless_runner_config: TestsRunnerConfig):
        self.headless_runner_config = actual_headless_runner_config
        self.__remaining_connection_attempts = actual_headless_runner_config.connection_attempts_number
        self.__start_headless_viriato()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__subprocess_running_headless is not None:
            self.safely_interrupt_headless()

    def __start_headless_viriato(self):
        headless_command_line_call = (
                self.headless_runner_config.headless_executable +
                ' ' +
                self.headless_runner_config.absolute_path_to_test_db +
                ' ' +
                self.headless_runner_config.config_file_on_relative_path)

        current_working_dir = os.getcwd()
        try:
            os.chdir(self.headless_runner_config.absolute_path_to_viriato)
            self.__subprocess_running_headless = subprocess.Popen(headless_command_line_call, shell=True)
        finally:
            os.chdir(current_working_dir)

    def check_and_wait_for_headless_to_be_ready(self, algorithm_interface: AlgorithmInterface):

        while self.__remaining_connection_attempts > 1:
            time.sleep(self.headless_runner_config.connection_retry_wait_seconds)
            try:
                algorithm_interface.notify_user('this_is_just', 'to_test_if_there_is_a_connection')
                break
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                print("Warning *** \n No connection to runner, trying once more in {0} seconds"
                      .format(self.headless_runner_config.connection_retry_wait_seconds))
                self.__remaining_connection_attempts -= 1
            except AlgorithmPlatformError as algorithm_platform_error_instance:
                print("Warning *** \n Algorithm Platform responded with an error {0}".format(
                    algorithm_platform_error_instance.message))
                break

        if self.__remaining_connection_attempts < 2:
            time.sleep(self.headless_runner_config.connection_retry_wait_seconds)
            print("Warning *** \n Could not connect to runner, final attempt \n")
            algorithm_interface.notify_user('this_is_just', 'to_test_if_there_is_a_connection')

        print("connected to runner on URL\n{0}\n".format(algorithm_interface.base_url))

    def check_if_headless_is_still_running(self) -> bool:
        process_is_still_running = self.__subprocess_running_headless.poll() is None
        return process_is_still_running

    def safely_interrupt_headless(self):
        if self.check_if_headless_is_still_running():
            try:
                self.__subprocess_running_headless.send_signal(signal.CTRL_C_EVENT)
                print('shutting down Headless')
                while self.check_if_headless_is_still_running():
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            print('Headless has been shut down successfully')
