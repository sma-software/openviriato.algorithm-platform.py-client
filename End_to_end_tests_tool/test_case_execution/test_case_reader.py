import json
from jsonpath_ng import parse
from jsonpath_ng.lexer import JsonPathLexerError
from typing import Dict
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase
from py_client.conversion.converter_helpers import _translate_key
from py_client.conversion.algorithm_platform_json_to_aidm_converter import convert
from End_to_end_tests_tool import result
from py_client.aidm import *


def _get_parameter_names_for_test_method(c_sharp_method_signature: str) -> List[str]:
    parameter_names_separated_by_comma = c_sharp_method_signature.split('(')[1].split(')')[0]
    untrimmed_parameter_keys = parameter_names_separated_by_comma.split(',')
    return [_translate_key(parameter_key.strip()) for parameter_key in untrimmed_parameter_keys]


def _evaluate_primitive_values_by_key_from_path_expressions(
        keys: List[str],
        path_expressions_by_keys: Dict[str, str],
        call_json: Dict[str, str]) -> result.Result:
    primitive_values_for_keys = []
    for key in keys:
        # maybe the case that a key is missing in the parameter mapping
        if key in path_expressions_by_keys.keys():
            value_mapping_expression = path_expressions_by_keys[key]
            try:
                parsed_expression = parse(value_mapping_expression)
            except JsonPathLexerError:
                return result.from_error("Can not parse jpath: {0}".format(value_mapping_expression))
            found_values = parsed_expression.find(call_json)
            if len(found_values) == 1:
                primitive_values_for_keys.append(found_values[0].value)
            else:
                if len(found_values) == 0:
                    return result.from_error("No value found for jpath {0}".format(value_mapping_expression))
                else:
                    return result.from_error("Ambiguous jpath: {0}".format(value_mapping_expression))

    extra_mapping_keys = [
        key for key in path_expressions_by_keys.keys() if key not in keys]
    if len(extra_mapping_keys) > 0:
        return result.from_error('Extra mapping keys: {0}'.format(", ".join(extra_mapping_keys)))

    return result.from_result(primitive_values_for_keys)


def _evaluate_python_object_mapping(py_method_parameter_names,
                                    py_object_path_expressions,
                                    call_json) -> result.Result:
    object_arguments = []
    for py_method_parameter_name in py_method_parameter_names:
        found_mappings = [
            object_mapping for object_mapping in py_object_path_expressions
            if "ParameterName" in object_mapping.keys() and
               object_mapping["ParameterName"] == py_method_parameter_name]
        if len(found_mappings) == 0:
            return result.from_error('Missing object mapping for parameter: {0}'.format(py_method_parameter_name))
        if len(found_mappings) > 1:
            return result.from_error('Multiple object mappings for parameter: {0}'.format(py_method_parameter_name))

        parameter_mapping_for_object = found_mappings[0]["PythonParameterMapping"]
        primitive_values = _evaluate_primitive_values_by_key_from_path_expressions(
            parameter_mapping_for_object.keys(),
            parameter_mapping_for_object,
            call_json)

        if "ClassName" not in found_mappings[0].keys():
            return result.from_error('Missing class name for parameter: {0}'.format(py_method_parameter_name))
        expected_class_name = found_mappings[0]['ClassName']

        primitive_values_by_parameter_keys = {
            key: primitive_values.result_value[i] for i, key in enumerate(parameter_mapping_for_object.keys())}
        try:
            expected_class = eval(expected_class_name)
            object_arguments.append(convert(expected_class, primitive_values_by_parameter_keys))
        except TypeError:
            return result.from_error("Conversion failed for class {0} in parameter {1}".format(
                expected_class_name,
                py_method_parameter_name))

    return result.from_result(object_arguments)


def _create_headless_test_case(call_json: dict, py_call_json: dict, expected_json: dict) -> EndToEndTestCase:
    c_sharp_method_signature: str = call_json['CSharpMethodName']
    py_method_name = _translate_key(c_sharp_method_signature.split('(')[0])
    py_method_parameter_names = _get_parameter_names_for_test_method(c_sharp_method_signature)

    if "PythonParameterMapping" in py_call_json.keys() and "PythonObjectMapping" in py_call_json.keys():
        raise NotImplementedError(
            "Unsupported Case with PythonParameterMapping and PythonObjectMapping in {0}".format(py_method_name))

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

    if "PythonParameterMapping" in py_call_json.keys():
        py_argument_path_expressions = py_call_json['PythonParameterMapping']
        arguments_for_method_to_test_result = _evaluate_primitive_values_by_key_from_path_expressions(
            py_method_parameter_names,
            py_argument_path_expressions,
            call_json)

        return EndToEndTestCase(
            name_of_method_to_test=py_method_name,
            py_client_argument_result=arguments_for_method_to_test_result,
            expected_response_as_json=expected_json)

    raise NotImplementedError(
        "Expected PythonParameterMapping or PythonObjectMapping in {0}".format(py_method_name))


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
