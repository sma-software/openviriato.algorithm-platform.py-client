import json
from jsonpath_ng import parse
from typing import List, Dict
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from py_client.Conversion.converter_helpers import _translate_key


def _get_parameter_names_for_test_method(c_sharp_method_signature: str) -> List[str]:
    parameter_names_separated_by_comma = c_sharp_method_signature.split('(')[1].split(')')[0]
    untrimmed_parameter_keys = parameter_names_separated_by_comma.split(',')
    return [_translate_key(parameter_key.strip()) for parameter_key in untrimmed_parameter_keys]


def _calculate_arguments_by_path_expressions(
        py_method_parameter_names: List[str],
        py_argument_path_expressions:  Dict[str, str],
        call_json: Dict[str, str]) -> List:
    py_client_parameters = []
    for parameter_name in py_method_parameter_names:
        # maybe the case that a parameter is missing in the parameter mapping
        if parameter_name in py_argument_path_expressions.keys():
            parameter_mapping_expression = py_argument_path_expressions[parameter_name]
            parsed_expression = parse(parameter_mapping_expression)
            py_client_parameters.append(parsed_expression.find(call_json)[0].value)
    return py_client_parameters


def _create_headless_test_case(call_json: dict, py_call_json: dict, expected_json: dict) -> EndToEndTestCase:
    c_sharp_method_signature: str = call_json['CSharpMethodName']
    py_method_name = _translate_key(c_sharp_method_signature.split('(')[0])
    py_method_parameter_names = _get_parameter_names_for_test_method(c_sharp_method_signature)

    py_argument_path_expressions = py_call_json['PythonParameterMapping']
    parameters_for_method_to_test = _calculate_arguments_by_path_expressions(
        py_method_parameter_names,
        py_argument_path_expressions,
        call_json)

    extra_mapping_parameters = [
        key for key in py_argument_path_expressions.keys() if key not in py_method_parameter_names]

    return EndToEndTestCase(
        name_of_method_to_test=py_method_name,
        py_client_parameters=parameters_for_method_to_test,
        expected_response_as_json=expected_json,
        extra_mapping_parameters=extra_mapping_parameters)


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
