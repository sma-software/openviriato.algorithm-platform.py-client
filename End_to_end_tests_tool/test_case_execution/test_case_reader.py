import json
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from End_to_end_tests_tool.test_case_execution.value_mapping_evaluators import _get_parameter_names_for_test_method, \
    _evaluate_primitive_values_by_key_from_path_expressions, _evaluate_python_object_mapping, \
    read_arguments_from_object_json
from py_client.conversion.converter_helpers import _translate_key
from End_to_end_tests_tool import result


def _create_headless_test_case(call_json: dict, py_call_json: dict, expected_json: dict) -> EndToEndTestCase:
    c_sharp_method_signature: str = call_json['CSharpMethodName']
    py_method_name = _translate_key(c_sharp_method_signature.split('(')[0])
    py_method_parameter_names = _get_parameter_names_for_test_method(c_sharp_method_signature)

    ALLOWED_KEYS = ["PythonParameterMapping", "PythonObjectMapping", "PythonParameterFromJson"]
    keys_not_in_allowed_set = [key for key in py_call_json.keys() if key not in ALLOWED_KEYS]
    if len(keys_not_in_allowed_set) > 0:
        raise NotImplementedError(
            "Invalid test case definition with unsupported attribute(s) {0} in {1}".format(
                ", ".join(keys_not_in_allowed_set),
                py_method_name))

    if "PythonObjectMapping" in py_call_json.keys():
        py_object_path_expressions = py_call_json['PythonObjectMapping']
        arguments_for_method_to_test_result = _evaluate_python_object_mapping(
            py_method_parameter_names,
            py_object_path_expressions,
            call_json)

        return EndToEndTestCase(
            name_of_method_to_test=py_method_name,
            py_client_argument_result=arguments_for_method_to_test_result,
            expected_response_as_json=expected_json)

    elif "PythonParameterMapping" in py_call_json.keys():
        py_argument_path_expressions = py_call_json['PythonParameterMapping']
        arguments_for_method_to_test_result = _evaluate_primitive_values_by_key_from_path_expressions(
            py_method_parameter_names,
            py_argument_path_expressions,
            call_json)

        return EndToEndTestCase(
            name_of_method_to_test=py_method_name,
            py_client_argument_result=arguments_for_method_to_test_result,
            expected_response_as_json=expected_json)

    elif "PythonParameterFromJson" in py_call_json.keys():
        arguments = py_call_json['PythonParameterFromJson']

        return EndToEndTestCase(
            name_of_method_to_test=py_method_name,
            py_client_argument_result=read_arguments_from_object_json(arguments),
            expected_response_as_json=expected_json)
    else:
        return EndToEndTestCase(
            name_of_method_to_test=py_method_name,
            py_client_argument_result=result.from_result([]),
            expected_response_as_json=expected_json)


def read_test_cases_from_calls_py_calls_and_expected(
        call_path: str,
        py_call_file_path: str,
        expected_file_path: str) -> EndToEndTestCase:
    def __read_json_file(path_to_json: str) -> dict:
        with open(path_to_json, encoding='utf-8-sig') as input_file:
            return json.loads(input_file.read())

    call_json = __read_json_file(call_path)
    py_call_json = __read_json_file(py_call_file_path)
    expected_json = __read_json_file(expected_file_path)

    return _create_headless_test_case(call_json, py_call_json, expected_json)
