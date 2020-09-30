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


class _PathTripleToDataPerEndToEndTest:
    __examples_file_path: str
    __py_call_file_path: str
    __expected_file_path: str

    def __init__(self, examples_file_path, py_call_file_path, expected_file_path):
        self.__examples_file_path = examples_file_path
        self.__py_call_file_path = py_call_file_path
        self.__expected_file_path = expected_file_path

    @property
    def examples_file_path(self) -> str:
        return self.__examples_file_path

    @property
    def py_call_file_path(self) -> str:
        return self.__py_call_file_path

    @property
    def expected_file_path(self) -> str:
        return self.__expected_file_path


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


def _create_list_of_path_triples_to_data_for_one_end_to_end_test_from_examples_file_paths(
        headless_runner_config: TestsRunnerConfig) -> List[_PathTripleToDataPerEndToEndTest]:
    def __extract_path_to_same_filename_in_list(paths_to_file: List[str], filename_to_find: str) -> Optional[str]:
        for i in range(len(paths_to_file)):
            if filename_to_find in paths_to_file[i]:
                return paths_to_file.pop(i)
        return None

    examples_json_files_with_path = __find_absolute_paths_of_jsons_in_data_subdir(
        headless_runner_config,
        TEST_CALL_DIRECTORY)
    py_call_json_files_with_path = __find_absolute_paths_of_jsons_in_data_subdir(
        headless_runner_config,
        PY_CALL_DIRECTORY)
    headless_runner_config = __find_absolute_paths_of_jsons_in_data_subdir(
        headless_runner_config,
        TEST_EXPECTED_DIRECTORY)

    path_triples: List[_PathTripleToDataPerEndToEndTest] = []
    for examples_file_path in examples_json_files_with_path:
        file_name = examples_file_path.split("\\")[-1]
        py_call_file_path = __extract_path_to_same_filename_in_list(py_call_json_files_with_path, file_name)
        expected_file_path = __extract_path_to_same_filename_in_list(headless_runner_config, file_name)

        if py_call_file_path is None:
            raise FileNotFoundError(
                "{0} does not have a corresponding file in {1}"
                "".format(file_name, os.path.dirname(py_call_json_files_with_path[0])))
        if expected_file_path is None:
            raise FileNotFoundError(
                "{0} does not have a corresponding file in {1}"
                "".format(file_name, os.path.dirname(headless_runner_config[0])))

        path_triples.append(_PathTripleToDataPerEndToEndTest(examples_file_path, py_call_file_path, expected_file_path))

    return path_triples


def run_end_to_end_tests_with_headless(
        headless_runner_config: TestsRunnerConfig,
        running_headless: headless_runner.ViriatoHeadlessRunner,
        file_to_store_test_results: Type[open]) -> List[EndToEndTestCaseResult]:
    base_url = 'http://localhost:{0}'.format(headless_runner_config.algorithm_interface_port_nr)

    with algorithm_interface_factory.create(base_url) as algorithm_interface:
        running_headless.check_and_wait_for_headless_to_be_ready(algorithm_interface)

        performed_tests = []
        test_case_reader = TestCaseReader(base_url)
        path_triple_per_test = _create_list_of_path_triples_to_data_for_one_end_to_end_test_from_examples_file_paths(
            headless_runner_config)
        for path_triple_for_one_test in path_triple_per_test:
            end_to_end_test_case = test_case_reader.read_test_cases_from_calls_py_calls_and_expected(
                path_triple_for_one_test.examples_file_path,
                path_triple_for_one_test.py_call_file_path,
                path_triple_for_one_test.expected_file_path)
            performed_tests.append(execute_test_case(algorithm_interface, end_to_end_test_case))

    print_all_test_case_statuses_and_messages_in_console_or_file(performed_tests)
    print_all_test_case_statuses_and_messages_in_console_or_file(performed_tests, file_to_store_test_results)
    return performed_tests


if __name__ == '__main__':
    run_end_to_end_test_with_running_algorithm_platform_in_mode_start_up_rest_interface_only()
