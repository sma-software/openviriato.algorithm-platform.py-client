from ConversionLayer.converter_helpers import check_and_format_any_datetime_to_iso_str, check_and_format_any_enum_to_str
import AIDMClasses.AIDM_classes


def convert_to_json_conform_dict(AIDM_object) -> dict:
    attribute_names = [attr for attr in dir(AIDM_object) if not attr.startswith('_')]
    attribute_dict = dict()
    for attribute_name in attribute_names:
        attribute_dict[attribute_name] = convert_to_json_conform_obj(getattr(AIDM_object, attribute_name))
    return attribute_dict


def convert_to_list_of_dict(list_of_AIDM_object: list) -> list:
    return [convert_to_json_conform_dict(AIDM_object) for AIDM_object in list_of_AIDM_object]


def convert_to_json_conform_obj(obj) -> dict:
    if isinstance(obj, list):
        obj = [convert_any_type_to_json_conform_dict(el) for el in obj]
    else:
        obj = check_and_format_any_datetime_to_iso_str(check_and_format_any_enum_to_str(obj))
    return obj


def convert_any_type_to_json_conform_dict(any_type_obj) -> dict:
    if hasattr(any_type_obj, "__module__"):
        if any_type_obj.__module__ == AIDMClasses.AIDM_classes.__name__:
            any_type_obj = convert_to_json_conform_dict(any_type_obj)
    return any_type_obj