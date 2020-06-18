from AlgorithmInterface import AlgorithmInterface
from Conversion import object_to_algorithm_platform_json_converter
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from End_to_end_tests_tool.test_case_execution.test_case_result import EndToEndTestCaseResult, TestCaseResultStatus, \
    ExecutedEndToEndTest
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
        return method_to_call(*headless_test_case.parameters_for_method_to_test)
    except TypeError as TypeErrorInstance:
        return TypeErrorInstance


def factory_executed_test_case_and_method_not_found(headless_test_case: EndToEndTestCase) -> ExecutedEndToEndTest:
    method_not_found_result = EndToEndTestCaseResult(TestCaseResultStatus['Error'], 'Method not Found on interface')
    return ExecutedEndToEndTest(headless_test_case, method_not_found_result)


def factory_executed_test_case_and_parameters_did_not_map(
        headless_test_case: EndToEndTestCase,
        TypeErrorInstance: TypeError
) -> ExecutedEndToEndTest:
    error_message = 'Parameters did not Map: {0}'.format(str(TypeErrorInstance))
    parameters_not_mapped_result = EndToEndTestCaseResult(TestCaseResultStatus['Error'], error_message)
    return ExecutedEndToEndTest(headless_test_case, parameters_not_mapped_result)


def factory_executed_test_case_with_failed_as_expected_and_call_mismatch(
        headless_test_case: EndToEndTestCase
) -> ExecutedEndToEndTest:
    error_message = 'Response of call and Expected did not match'
    failed_test_result = EndToEndTestCaseResult(TestCaseResultStatus['Failed'], error_message)
    return ExecutedEndToEndTest(headless_test_case, failed_test_result)


def factory_executed_test_case_successful(headless_test_case: EndToEndTestCase) -> ExecutedEndToEndTest:
    successful_result = EndToEndTestCaseResult(TestCaseResultStatus['Success'], '')
    return ExecutedEndToEndTest(headless_test_case, successful_result)


def execute_test_case(
        algorithm_interface: AlgorithmInterface,
        headless_test_case: EndToEndTestCase
) -> ExecutedEndToEndTest:

    method_to_call = determine_method_to_test_on_algorithm_interface(algorithm_interface, headless_test_case)
    method_not_found = method_to_call is None
    if method_not_found:
        return factory_executed_test_case_and_method_not_found(headless_test_case)

    result = perform_test_request_on_algorithm_interface(method_to_call, headless_test_case)
    parameters_did_not_map = isinstance(result, TypeError)
    if parameters_did_not_map:
        return factory_executed_test_case_and_parameters_did_not_map(headless_test_case, result)

    result_as_json = object_to_algorithm_platform_json_converter.convert_any_object(result)
    if result_as_json == headless_test_case.expected_response_as_json:
        return factory_executed_test_case_successful(headless_test_case)
    else:
        return factory_executed_test_case_with_failed_as_expected_and_call_mismatch(headless_test_case)
