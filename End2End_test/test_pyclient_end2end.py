import os
import Conversion.object_to_algorithm_platform_json_converter as object_to_algorithm_platform_json_converter
from AlgorithmInterface import create
from End2End_test.headless_runner import ViriatoHeadlessRunnerConfig, ViriatoHeadlessRunner
from End2End_test.headless_test_case_provider import HeadLessTestCase, load_test_cases_from_calls_and_pyexpected
from End2End_test.loaders_for_json_files import load_test_config_file_port_number


def test_py_client_call(algorithm_interface, headless_test_case: HeadLessTestCase):
    response_object = headless_test_case.perform_test_request_on_algorithm_interface(algorithm_interface)
    response_as_json = object_to_algorithm_platform_json_converter.convert_any_object(response_object)

    try:
        assert (response_as_json == headless_test_case.expected_response_as_json)
        print("Test of " + headless_test_case.name_of_method_to_test + ' passed \n')
    except AssertionError:
        print("Test of " + headless_test_case.name_of_method_to_test + ' failed \n')


def main():
    headless_runner_config = ViriatoHeadlessRunnerConfig(
        config_file_with_relative_path="headless_cfg.json",
        test_db_with_absolute_path="C:\\Workspace\\AlgorithmPlatformInterfacePython\\End2EndTest\\"
                                   "BeispieldatenbankZürich-1.00.mdb",
        absolute_path_to_viriato="C:\\Workspace\\AlgorithmPlatformInterfacePython\\End2EndTest\\"
                                 "SMA.Viriato.Standard-1.0.16773.test")

    script_file_directory = os.path.dirname(os.path.realpath(__file__))
    BASE_URL = 'http://localhost:{0}'.format(load_test_config_file_port_number(headless_runner_config))
    headless_test_cases = load_test_cases_from_calls_and_pyexpected(script_file_directory)

    with ViriatoHeadlessRunner(headless_runner_config) as headless_runner:

        with create(BASE_URL) as algorithm_interface:
            headless_runner.check_and_wait_for_headless_to_be_ready(algorithm_interface)

            for headless_test_case in headless_test_cases:
                test_py_client_call(algorithm_interface, headless_test_case)


if __name__ == '__main__':
    main()
