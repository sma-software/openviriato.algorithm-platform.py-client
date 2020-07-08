import enum

import py_client
from Conversion.converter_helpers import convert_to_datetime_format_or_return_self, _convert_to_camel_case


def get_attribute_name_without_class_prefix(attribute_name_with_prefix):
    last_occurrence_double_underscore = attribute_name_with_prefix.rfind('__')
    return attribute_name_with_prefix[last_occurrence_double_underscore + 2:]


def convert_any_AIDM_object_to_dict(AIDM_object) -> dict:
    attribute_dict = dict()
    for attribute_name_with_class_prefix, value in AIDM_object.__dict__.items():
        attribute_name = get_attribute_name_without_class_prefix(attribute_name_with_class_prefix)
        attribute_dict[_convert_to_camel_case(attribute_name)] = convert_any_object(
            getattr(AIDM_object, attribute_name))
    return attribute_dict


def convert_any_object(obj):
    if isinstance(obj, list):
        return [convert_any_object(el) for el in obj]

    if isinstance(obj, enum.Enum):
        return _convert_to_camel_case(obj.name)

    is_from_AIDM_package = hasattr(obj, "__module__") and obj.__module__.split('.')[0] == py_client.__name__
    if is_from_AIDM_package:
        return convert_any_AIDM_object_to_dict(obj)
    else:
        return convert_to_datetime_format_or_return_self(obj)
