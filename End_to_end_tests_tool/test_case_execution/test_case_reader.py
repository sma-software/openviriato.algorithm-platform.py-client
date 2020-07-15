import json
from jsonpath_ng import parse
from typing import List, Dict
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from py_client.Conversion.converter_helpers import _translate_key


def _get_parameter_names_for_test_method(c_sharp_method_signature: str) -> List[str]:
    parameter_names_separated_by_comma = c_sharp_method_signature.split('(')[1].split(')')[0]
    untrimmed_parameter_keys = parameter_names_separated_by_comma.split(',')
    return [_translate_key(parameter_key.strip()) for parameter_key in untrimmed_parameter_keys]


def _get_parameters_by_name_and_mapping(
        py_client_test_parameter_names: List[str],
        py_client_mappings: Dict[str, Dict[str, str]],
        test_call_json: Dict[str, str]) -> List:
    py_client_parameters = []
    for parameter_name in py_client_test_parameter_names:
        if parameter_name not in py_client_mappings['PythonParameterMapping'].keys():
            continue
        parameter_mapping_expression = py_client_mappings['PythonParameterMapping'][parameter_name]
        parsed_expression = parse(parameter_mapping_expression)
        py_client_parameters.append(parsed_expression.find(test_call_json)[0].value)
    return py_client_parameters


def _create_headless_test_case(c_sharp_call_json: dict, py_call_json: dict, expected_json: dict) -> EndToEndTestCase:
    c_sharp_method_signature: str = c_sharp_call_json['CSharpMethodName']
    py_client_test_method_name = _translate_key(c_sharp_method_signature.split('(')[0])
    py_client_test_parameter_names = _get_parameter_names_for_test_method(c_sharp_method_signature)

    parameters_for_method_to_test = _get_parameters_by_name_and_mapping(
        py_client_test_parameter_names,
        py_call_json,
        c_sharp_call_json)

    headless_test_case = EndToEndTestCase(
        name_of_method_to_test=py_client_test_method_name,
        py_client_parameters=parameters_for_method_to_test,
        expected_response_as_json=expected_json,
        extra_mapping_parameters=[])

    return headless_test_case


def read_test_cases_from_calls_py_calls_and_expected(
        c_sharp_call_path: str,
        py_call_file_path: str,
        expected_file_path: str) -> EndToEndTestCase:
    def __read_json_file(path_to_json: str) -> dict:
        with open(path_to_json, encoding='utf-8-sig') as input_file:
            return json.loads(input_file.read())

    c_sharp_call_json = __read_json_file(c_sharp_call_path)
    py_call_json = __read_json_file(py_call_file_path)
    expected_json = __read_json_file(expected_file_path)

    return _create_headless_test_case(c_sharp_call_json, py_call_json, expected_json)
