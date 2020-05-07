import json
import os
from typing import List, Union
from AlgorithmInterface import AlgorithmInterface


class HeadLessTestCase:
    name_of_test_case: str
    name_of_method_to_test: str
    parameters_for_method_to_test: list
    expected_response_as_json: Union[list, dict]

    def __init__(self,
                 name_of_test_case: str,
                 name_of_method_to_test: str,
                 parameters_for_method_to_test,
                 expected_response_as_json):
        self.name_of_test_case = name_of_test_case
        self.name_of_method_to_test = name_of_method_to_test
        self.parameters_for_method_to_test = parameters_for_method_to_test
        self.expected_response_as_json = expected_response_as_json

    def perform_test_request_on_algorithm_interface(self, algorithm_interface: AlgorithmInterface):
        return getattr(algorithm_interface, self.name_of_method_to_test)(*self.parameters_for_method_to_test)


def load_test_cases_from_calls_and_pyexpected(main_script_directory) -> List[HeadLessTestCase]:
    path_to_calls = os.path.join(main_script_directory, "calls")
    path_to_expected = os.path.join(main_script_directory, "pyexpected")
    list_of_test_cases = []

    for call_directory in os.listdir(path_to_calls):
        call_category_path = os.path.join(path_to_calls, call_directory)
        expected_category_path = os.path.join(path_to_expected, call_directory)
        test_case_files = os.listdir(call_category_path)
        for test_case_file_name in test_case_files:
            with open(os.path.join(call_category_path, test_case_file_name), encoding='utf-8-sig') as input_file:
                call_as_json = json.loads(input_file.read())

            with open(os.path.join(expected_category_path, test_case_file_name), encoding='utf-8-sig') as input_file:
                expected_as_json = json.loads(input_file.read())

            headless_test_case = create_headless_test_case(test_case_file_name, call_as_json, expected_as_json)

            list_of_test_cases.append(headless_test_case)

    return list_of_test_cases


def create_headless_test_case(test_case_file_name, call_json, expected_json):
    parameters_for_method_to_test = convert_parameters_according_to_type(call_json['urlParameters'],
                                                                         call_json['PythonMethodParameterTypes'])
    name_of_method_to_test = call_json['PythonMethodName'].split('(')[0]
    headless_test_case = HeadLessTestCase(
        name_of_test_case=test_case_file_name,
        name_of_method_to_test=name_of_method_to_test,
        parameters_for_method_to_test=parameters_for_method_to_test,
        expected_response_as_json=expected_json)
    return headless_test_case


def convert_parameters_according_to_type(parameter_list: list, parameter_types: list) -> list:
    converted_parameters = []
    for parameter, type_name in zip(parameter_list, parameter_types):
        if isinstance(parameter, list):
            convert_parameters_according_to_type(parameter, type_name)
            converted_parameters.append(eval('{0}(*{1})'.format(type_name, parameter)))
        else:
            converted_parameters.append(eval('{0}({1})'.format(type_name, parameter)))
    return converted_parameters
