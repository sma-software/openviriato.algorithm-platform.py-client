from AlgorithmInterface import AlgorithmInterface
from Conversion import object_to_algorithm_platform_json_converter
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from End_to_end_tests_tool.test_case_execution.test_case_result import HeadlessTestCaseResult, TestCaseResultStatus


def determine_method_to_test_on_algorithm_interface(
        algorithm_interface: AlgorithmInterface,
        headless_test_case: EndToEndTestCase):
    return getattr(algorithm_interface, headless_test_case.name_of_method_to_test)


def perform_test_request_on_algorithm_interface(method_to_call, headless_test_case: EndToEndTestCase):
    return method_to_call(*headless_test_case.parameters_for_method_to_test)


def update_test_status_to_method_not_found_error(headless_test_case: EndToEndTestCase) -> EndToEndTestCase:
    attribute_error_test_result = HeadlessTestCaseResult(TestCaseResultStatus['Error'], 'Method not Found on interface')
    headless_test_case.update_test_result_when_performed(attribute_error_test_result)
    return headless_test_case


def update_test_status_to_parameters_did_not_map_error(headless_test_case: EndToEndTestCase) -> EndToEndTestCase:
    not_mapped_error_test_result = HeadlessTestCaseResult(TestCaseResultStatus['Error'], 'Parameters did not Map')
    headless_test_case.update_test_result_when_performed(not_mapped_error_test_result)
    return headless_test_case


def update_test_status_to_failed_as_expected_and_call_mismatch(headless_test_case: EndToEndTestCase) -> EndToEndTestCase:
    failed_with_mismatch_test_result = HeadlessTestCaseResult(
        TestCaseResultStatus['Failed'],
        'Response of call and Expected did not match')
    headless_test_case.update_test_result_when_performed(failed_with_mismatch_test_result)
    return headless_test_case


def update_test_status_to_test_successful(headless_test_case: EndToEndTestCase) -> EndToEndTestCase:
    successful_result = HeadlessTestCaseResult(TestCaseResultStatus['Success'], '')
    headless_test_case.update_test_result_when_performed(successful_result)
    return headless_test_case


def execute_test_case(
        algorithm_interface: AlgorithmInterface,
        headless_test_case: EndToEndTestCase
) -> EndToEndTestCase:
    # aufzurufende methode mit Parametern bestimmen vom headless_test_case
    try:
        method_to_call = determine_method_to_test_on_algorithm_interface(algorithm_interface, headless_test_case)
    except AttributeError:
        return update_test_status_to_method_not_found_error(headless_test_case)

    # aufruf result = (method_to_call, parameter)
    try:
        result = perform_test_request_on_algorithm_interface(method_to_call, headless_test_case)
    except TypeError:
        return update_test_status_to_parameters_did_not_map_error(headless_test_case)

    # testen result.json == expected.json
    result_as_json = object_to_algorithm_platform_json_converter.convert_any_object(result)
    if result_as_json == headless_test_case.expected_response_as_json:
        return update_test_status_to_test_successful(headless_test_case)
    else:
        return update_test_status_to_failed_as_expected_and_call_mismatch(headless_test_case)
