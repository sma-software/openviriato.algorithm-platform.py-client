import os
from typing import List
from AlgorithmInterface import AlgorithmInterfaceFactory
from End_to_end_tests_tool.runner import tests_runner_config_file_reader, headless_runner
from End_to_end_tests_tool.runner.tests_runner_config import TestsRunnerConfig
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from End_to_end_tests_tool.test_case_execution.test_case_executor import execute_test_case
from End_to_end_tests_tool.test_case_execution.test_case_reader import read_test_cases_from_calls_and_pyexpected

TEST_CALL_DIRECTORY = 'calls'
TEST_EXPECTED_DIRECTORY = 'expected'

# TODO: später hier gesamtergebnis herausgeben
def print_all_test_case_statuses_and_messages_in_console(performed_tests: List[EndToEndTestCase]):
    print('End to End Test results \n')
    for case in performed_tests:
        print(case.test_case_name)
        print(case.name_of_method_to_test)
        print(case.test_result.test_case_result_status.name)
        print(case.test_result.error_message)
        print('----')


def __find_absolute_paths_of_jsons_in_data_subdir(headless_runner_config: TestsRunnerConfig, subdir: str) -> List[str]:
    path_to_subdir = os.path.join(headless_runner_config.data_root_path_relative, subdir)
    return [os.path.join(path, name)
            for path, subdirs, files in os.walk(path_to_subdir)
            for name in files if name.endswith('.json')]


def run_end_to_end_tests(configuration_file_path: str) -> List[EndToEndTestCase]:
    root_directory = os.path.dirname(os.path.realpath(__file__))

    headless_runner_config: TestsRunnerConfig = tests_runner_config_file_reader.read_headless_runner_config_from_config_file(
        root_directory,
        configuration_file_path)

    with headless_runner.ViriatoHeadlessRunner(headless_runner_config) as running_headless:
        base_url = 'http://localhost:{0}'.format(headless_runner_config.algorithm_interface_port_nr)

        with AlgorithmInterfaceFactory.create(base_url) as algorithm_interface:
            running_headless.check_and_wait_for_headless_to_be_ready(algorithm_interface)

            examples_json_files_with_path = __find_absolute_paths_of_jsons_in_data_subdir(
                headless_runner_config,
                TEST_CALL_DIRECTORY)
            expected_json_files_with_path = __find_absolute_paths_of_jsons_in_data_subdir(
                headless_runner_config,
                TEST_EXPECTED_DIRECTORY)

            performed_tests = []
            for examples_file_path, expected_file_path in \
                    zip(examples_json_files_with_path, expected_json_files_with_path):
                end_to_end_test_case = read_test_cases_from_calls_and_pyexpected(examples_file_path, expected_file_path)
                performed_tests.append(execute_test_case(algorithm_interface, end_to_end_test_case))

    print_all_test_case_statuses_and_messages_in_console(performed_tests)
    return performed_tests
