import datetime

import isodate


def check_for_datetime(obj):
    if isinstance(obj, datetime.datetime):
        obj = obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        obj = isodate.duration_isoformat(obj)
    return obj

def convert_to_json_conform_dict(AIDM_object) -> dict:
    attribute_names = [attr for attr in dir(AIDM_object) if not attr.startswith('_')]
    attribute_dict = dict()
    for attribute_name in attribute_names:
        attribute_dict[attribute_name] = check_for_datetime(getattr(AIDM_object, attribute_name))
    return attribute_dict



def convert_to_list_of_dict(list_of_AIDM_object: list) -> list:
    l = [convert_to_json_conform_dict(AIDM_object) for AIDM_object in list_of_AIDM_object]
    return l
