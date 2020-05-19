import json
from typing import List
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase


def __convert_parameters_according_to_type(parameter_list: list, parameter_types: list) -> List[object]:
    converted_parameters = []
    for parameter, type_name in zip(parameter_list, parameter_types):
        if isinstance(parameter, list):
            __convert_parameters_according_to_type(parameter, type_name)
            converted_parameters.append(eval('{0}(*{1})'.format(type_name, parameter)))
        else:
            converted_parameters.append(eval('{0}({1})'.format(type_name, parameter)))
    return converted_parameters


def __create_headless_test_case(test_case_file_name, call_json, expected_json) -> EndToEndTestCase:
    parameters_for_method_to_test = __convert_parameters_according_to_type(call_json['urlParameters'],
                                                                           call_json['PythonMethodParameterTypes'])
    name_of_method_to_test = call_json['PythonMethodName'].split('(')[0]
    headless_test_case = EndToEndTestCase(
        name_of_test_case=test_case_file_name,
        name_of_method_to_test=name_of_method_to_test,
        parameters_for_method_to_test=parameters_for_method_to_test,
        expected_response_as_json=expected_json)
    return headless_test_case


def read_test_cases_from_calls_and_pyexpected(examples_file_path: str, expected_file_path: str) -> EndToEndTestCase:

    with open(examples_file_path, encoding='utf-8-sig') as input_file:
        call_as_json = json.loads(input_file.read())
    with open(expected_file_path, encoding='utf-8-sig') as input_file:
        expected_as_json = json.loads(input_file.read())

    return __create_headless_test_case(examples_file_path, call_as_json, expected_as_json)





