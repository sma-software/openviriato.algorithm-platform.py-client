import datetime

import isodate


def check_attributes_by_list(obj, attribute_names: list):
    for attribute_name in attribute_names:
        assert (hasattr(obj, attribute_name)), 'attribute {0} is missing'.format(attribute_name)


def parse_to_datetime(datetime_raw_str: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(datetime_raw_str)


def parse_to_timedelta(timedelta_raw_str: str) -> datetime.timedelta:
    return isodate.parse_duration(timedelta_raw_str)


def parse_to_timedelta_or_None(timedelta_raw_str: (str, None)) -> (datetime.timedelta, None):
    if timedelta_raw_str is not None:
        return isodate.parse_duration(timedelta_raw_str)
    else:
        return None
