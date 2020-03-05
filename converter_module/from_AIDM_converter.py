def remove_leading_and_trailing_underscore_from_keys(any_dict: dict) -> dict:
    for old_key in any_dict.keys():
        new_key = old_key.strip('__')
        any_dict[new_key] = any_dict.pop(old_key)

    return any_dict


def convert_to_dict(AIDM_object) -> dict:
    return remove_leading_and_trailing_underscore_from_keys(AIDM_object.__dict__)


def convert_to_list_of_dict(list_of_AIDM_object: list) -> list:
    return [convert_to_dict(AIDM_object) for AIDM_object in list_of_AIDM_object]


