import datetime


def check_attributes_by_list(obj, attribute_names: list):
    for attribute_name in attribute_names:
        assert (hasattr(obj, attribute_name)), 'attribute {0} is missing'.format(attribute_name)


def adjust_dict_keys_for_hidden_objects(json_as_dict: dict) -> dict:
    for old_key in json_as_dict.keys():
        new_key = '__{0}'.format(old_key)
        json_as_dict[new_key] = json_as_dict.pop(old_key)
    return json_as_dict


def parse_to_datetime(datetime_raw_str: str) -> datetime.datetime:
    return datetime.datetime.strptime(datetime_raw_str, '%Y-%m-%dT%H:%M:%S')