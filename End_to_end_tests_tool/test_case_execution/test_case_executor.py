from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.Conversion import object_to_algorithm_platform_json_converter
from py_client.communication.response_processing import AlgorithmPlatformError
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from End_to_end_tests_tool.test_case_execution.test_case_result import EndToEndTestCaseResult, TestCaseResultStatus
from typing import Optional


def determine_method_to_test_on_algorithm_interface(
        algorithm_interface: AlgorithmInterface,
        headless_test_case: EndToEndTestCase
) -> Optional[object]:
    is_method = hasattr(algorithm_interface, headless_test_case.name_of_method_to_test)
    if is_method:
        return getattr(algorithm_interface, headless_test_case.name_of_method_to_test)
    else:
        return None


def perform_test_request_on_algorithm_interface(method_to_call, headless_test_case: EndToEndTestCase) -> object:
    try:
        return method_to_call(*headless_test_case.arguments_for_py_client_method_result.result_value)
    except TypeError as type_error_instance:
        return type_error_instance
    except AlgorithmPlatformError as algorithm_platform_error_instance:
        return algorithm_platform_error_instance


def execute_test_case(
        algorithm_interface: AlgorithmInterface,
        headless_test_case: EndToEndTestCase
) -> EndToEndTestCaseResult:
    method_to_call = determine_method_to_test_on_algorithm_interface(algorithm_interface, headless_test_case)

    if method_to_call is None:
        return EndToEndTestCaseResult(
            result_status=TestCaseResultStatus.Error,
            error_message='Method not found error',
            invoked_method_name=headless_test_case.name_of_method_to_test,
            applied_arguments_result=headless_test_case.arguments_for_py_client_method_result)

    if not headless_test_case.arguments_for_py_client_method_result.is_success:
        return EndToEndTestCaseResult(
            result_status=TestCaseResultStatus.Error,
            error_message=headless_test_case.arguments_for_py_client_method_result.error_message,
            invoked_method_name=headless_test_case.name_of_method_to_test,
            applied_arguments_result=headless_test_case.arguments_for_py_client_method_result)

    response_as_aidm = perform_test_request_on_algorithm_interface(method_to_call, headless_test_case)

    if isinstance(response_as_aidm, TypeError):
        return EndToEndTestCaseResult(
            result_status=TestCaseResultStatus.Error,
            error_message='Arguments did not map, correct py_call argument mapping',
            invoked_method_name=headless_test_case.name_of_method_to_test,
            applied_arguments_result=headless_test_case.arguments_for_py_client_method_result)

    if isinstance(response_as_aidm, AlgorithmPlatformError):
        return EndToEndTestCaseResult(
            result_status=TestCaseResultStatus.Failed,
            error_message='Algorithm Platform returned an Error: {0}'.format(response_as_aidm.message),
            invoked_method_name=headless_test_case.name_of_method_to_test,
            applied_arguments_result=headless_test_case.arguments_for_py_client_method_result)

    result_as_json = object_to_algorithm_platform_json_converter.convert_any_object(response_as_aidm)
    if result_as_json == headless_test_case.expected_response_as_json:
        return EndToEndTestCaseResult(
            result_status=TestCaseResultStatus.Success,
            error_message=None,
            invoked_method_name=headless_test_case.name_of_method_to_test,
            applied_arguments_result=headless_test_case.arguments_for_py_client_method_result)
    else:
        return EndToEndTestCaseResult(
            result_status=TestCaseResultStatus.Failed,
            error_message='Assertion Error: result does not match expected',
            invoked_method_name=headless_test_case.name_of_method_to_test,
            applied_arguments_result=headless_test_case.arguments_for_py_client_method_result)
