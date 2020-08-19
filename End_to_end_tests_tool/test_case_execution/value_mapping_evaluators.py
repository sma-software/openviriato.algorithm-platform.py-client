from typing import Dict

from jsonpath_ng import parse
from jsonpath_ng.lexer import JsonPathLexerError
from requests import get

from End_to_end_tests_tool import result
from py_client.conversion.algorithm_platform_json_to_aidm_converter import *
from py_client.conversion.convert_json_to_aidm_for_end_to_end_test_tools import *
from py_client.conversion.converter_helpers import _translate_key


def _get_parameter_names_for_test_method(c_sharp_method_signature: str) -> List[str]:
    parameter_names_separated_by_comma = c_sharp_method_signature.split('(')[1].split(')')[0]
    untrimmed_parameter_keys = parameter_names_separated_by_comma.split(',')
    return [_translate_key(parameter_key.strip()) for parameter_key in untrimmed_parameter_keys]


def _get_parameter_value_from_algorithm_platform(parameter_name: str,
                                                 path_expression_to_parameter: str) -> result.Result:
    response = get("http://localhost:8089/parameters/{0}".format(parameter_name))

    if response.status_code != 200:
        return result.from_error(
            "status code {0}, could not get value for parameter {1}:{2} from algorithm platform".format(
                response.status_code, parameter_name, path_expression_to_parameter))
    else:
        return _extract_value_with_path_expression(response.json()["Value"], path_expression_to_parameter)


def _extract_value_with_path_expression(call_json: dict, path_expression: str) -> result.Result:
    try:
        parsed_expression = parse(path_expression)
    except JsonPathLexerError:
        return result.from_error("Can not parse jpath: {0}".format(path_expression))
    found_values = parsed_expression.find(call_json)

    if len(found_values) == 1:
        return result.from_result(found_values[0].value)
    else:
        if len(found_values) == 0:
            return result.from_error("No value found for jpath {0}".format(path_expression))
        else:
            return result.from_error("Ambiguous jpath: {0}".format(path_expression))


def _evaluate_primitive_values_by_key_from_path_expressions(
        keys: List[str],
        path_expressions_by_keys: Dict[str, str],
        call_json: Dict[str, str]) -> result.Result:

    primitive_values_for_keys = []
    for key in keys:
        # maybe the case that a key is missing in the parameter mapping
        if key in path_expressions_by_keys.keys():
            value_mapping_expression = path_expressions_by_keys[key]
            result_value = _extract_value_with_path_expression(call_json, value_mapping_expression)

            if result_value.is_success:
                result_value = result_value.result_value
                value_is_a_parameter_from_algorithm_platform = (
                        isinstance(result_value, str) and result_value.startswith("=") and result_value.endswith("="))

                if value_is_a_parameter_from_algorithm_platform:
                    parameter_with_path_expression: str = result_value.strip("=")
                    parameter_name = parameter_with_path_expression.split(":")[0]
                    path_expression = parameter_with_path_expression[len(parameter_name) + 1:]
                    parameter_value = _get_parameter_value_from_algorithm_platform(parameter_name, path_expression)
                    if parameter_value.is_success:
                        primitive_values_for_keys.append(parameter_value.result_value)
                    else:
                        return parameter_value
                else:
                    primitive_values_for_keys.append(result_value)
            else:
                return result_value

    extra_mapping_keys = [key for key in path_expressions_by_keys.keys() if key not in keys]
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

        if not primitive_values.is_success:
            return primitive_values

        primitive_values_by_parameter_keys = {
            key: primitive_values.result_value[i] for i, key in enumerate(parameter_mapping_for_object.keys())}
        try:
            expected_class = eval(expected_class_name)
        except NameError:
            return result.from_error("Class {0} is not defined for {1}".format(
                expected_class_name,
                py_method_parameter_name))
        try:
            object_arguments.append(convert(expected_class, primitive_values_by_parameter_keys))
        except TypeError:
            return result.from_error("Conversion failed for class {0} in parameter {1}".format(
                expected_class_name,
                py_method_parameter_name))

    return result.from_result(object_arguments)


def read_arguments_from_object_json(arguments: List[dict]) -> result.Result:
    result_list = []
    for argument in arguments:
        if "ObjectJson" not in argument.keys():
            return result.from_error('No object json defined')
        object_as_json = argument["ObjectJson"]
        if "aidm_factory" not in argument.keys():
            return result.from_error('No aidm_factory defined')

        factory_method_name: str = argument["aidm_factory"]
        if factory_method_name is not None and factory_method_name != "":
            try:
                factory_method = eval(factory_method_name)
            except NameError:
                return result.from_error("Factory method {0} not found ".format(factory_method_name))

            try:
                result_list.append(convert(factory_method, object_as_json))
            except (TypeError, ValueError):
                return result.from_error("Could not convert object json with factory method {0}".format(
                    factory_method_name))
            except KeyError as key_error_instance:
                return result.from_error("Could not convert object json with factory method {0}, KeyError {1}".format(
                    factory_method_name, str(key_error_instance)))

    return result.from_result(result_list)
