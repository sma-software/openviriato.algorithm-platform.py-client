import os
from typing import List, Optional, Type

from End_to_end_tests_tool.runner import tests_runner_config_file_reader, headless_runner
from End_to_end_tests_tool.runner.tests_runner_config import TestsRunnerConfig
from End_to_end_tests_tool.test_case_execution.test_case_executor import execute_test_case
from End_to_end_tests_tool.test_case_execution.test_case_reader import TestCaseReader
from End_to_end_tests_tool.test_case_execution.test_case_result import EndToEndTestCaseResult
from py_client.algorithm_interface import algorithm_interface_factory

TEST_CALL_DIRECTORY = 'calls'
PY_CALL_DIRECTORY = 'py_calls'
TEST_EXPECTED_DIRECTORY = 'expected'


def print_all_test_case_statuses_and_messages_in_console_or_file(
        performed_tests: List[EndToEndTestCaseResult],
        file_to_store_results: Optional[Type[open]] = None):
    def print_to_file_or_console(object_to_print: object):
        print(object_to_print, file=file_to_store_results)

    print_to_file_or_console('End to End Test results \n')
    number_of_failed_or_erroneous_tests = 0
    for result in performed_tests:
        if not result.test_case_result_status == result.test_case_result_status.Success:
            number_of_failed_or_erroneous_tests += 1
        print_to_file_or_console("Method:         {0}".format(result.invoked_method_name))
        print_to_file_or_console("Status:         {0}".format(result.test_case_result_status.name))
        if result.applied_arguments_result.is_success:
            print_to_file_or_console("Arguments:      {0}".format(result.applied_arguments_result.result_value))
        else:
            print_to_file_or_console("Argument Error: {0}".format(result.applied_arguments_result.error_message))
            number_of_failed_or_erroneous_tests += 1
        print_to_file_or_console("Message:        {0}".format(result.error_message))
        print_to_file_or_console('----')

    print_to_file_or_console('----')
    if number_of_failed_or_erroneous_tests == 0:
        print_to_file_or_console(
            "Summary:        All End-To-End-Tests were executed successfully. There are no errors and no test fails")
    else:
        print_to_file_or_console(
            "Summary:        In total {0} End-To-End-Tests fail or lead to an error".format(
                number_of_failed_or_erroneous_tests))
    print_to_file_or_console('----\n----')


def __find_absolute_paths_of_jsons_in_data_subdir(headless_runner_config: TestsRunnerConfig, subdir: str) -> List[str]:
    path_to_subdir = os.path.join(headless_runner_config.data_root_path_relative, subdir)
    return [os.path.join(path, name)
            for path, subdirs, files in os.walk(path_to_subdir)
            for name in files if name.endswith('.json')]


# Use in IDE as unittest or invoked by main from command-line
def run_end_to_end_tests(
        configuration_file_path: str,
        relative_path_to_viriato_folder: str,
        relative_path_to_test_data_base: str,
        file_to_store_test_results: Type[open]) -> List[EndToEndTestCaseResult]:
    headless_runner_config = tests_runner_config_file_reader.read_headless_runner_config_from_config_file(
        configuration_file_path,
        relative_path_to_viriato_folder,
        relative_path_to_test_data_base)

    with headless_runner.ViriatoHeadlessRunner(headless_runner_config) as running_headless:
        return run_end_to_end_tests_with_headless(headless_runner_config, running_headless, file_to_store_test_results)


# For debugging purposes:
def run_end_to_end_test_with_running_algorithm_platform_in_mode_start_up_rest_interface_only():
    class HeadLessRunnerMock:

        def check_and_wait_for_headless_to_be_ready(self, algorithm_interface):
            pass

    os.chdir(os.path.dirname(os.path.dirname(__file__)))

    headless_runner_config = tests_runner_config_file_reader.read_headless_runner_config_from_config_file(
        "../",
        "runner/tests_runner_config.json")

    with open("mock_results.log", "w") as log_file:
        run_end_to_end_tests_with_headless(headless_runner_config, HeadLessRunnerMock(), log_file)


def run_end_to_end_tests_with_headless(
        headless_runner_config: TestsRunnerConfig,
        running_headless: headless_runner.ViriatoHeadlessRunner,
        file_to_store_test_results: Type[open]) -> List[EndToEndTestCaseResult]:
    base_url = 'http://localhost:{0}'.format(headless_runner_config.algorithm_interface_port_nr)

    with algorithm_interface_factory.create(base_url) as algorithm_interface:
        running_headless.check_and_wait_for_headless_to_be_ready(algorithm_interface)

        examples_json_files_with_path = __find_absolute_paths_of_jsons_in_data_subdir(
            headless_runner_config,
            TEST_CALL_DIRECTORY)
        py_call_json_files_with_path = __find_absolute_paths_of_jsons_in_data_subdir(
            headless_runner_config,
            PY_CALL_DIRECTORY)
        expected_json_files_with_path = __find_absolute_paths_of_jsons_in_data_subdir(
            headless_runner_config,
            TEST_EXPECTED_DIRECTORY)

        performed_tests = []
        test_case_reader = TestCaseReader(base_url)
        for examples_file_path, py_call_file_path, expected_file_path, in \
                zip(examples_json_files_with_path, py_call_json_files_with_path, expected_json_files_with_path):
            end_to_end_test_case = test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
                examples_file_path,
                py_call_file_path,
                expected_file_path)
            performed_tests.append(execute_test_case(algorithm_interface, end_to_end_test_case))

    print_all_test_case_statuses_and_messages_in_console_or_file(performed_tests)
    print_all_test_case_statuses_and_messages_in_console_or_file(performed_tests, file_to_store_test_results)
    return performed_tests


if __name__ == '__main__':
    run_end_to_end_test_with_running_algorithm_platform_in_mode_start_up_rest_interface_only()
