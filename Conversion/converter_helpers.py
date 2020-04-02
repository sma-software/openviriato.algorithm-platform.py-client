import datetime

import isodate


def parse_to_datetime(datetime_raw_str: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(datetime_raw_str)


def parse_to_timedelta(timedelta_raw_str: str) -> datetime.timedelta:
    return isodate.parse_duration(timedelta_raw_str)


def parse_to_timedelta_or_None(timedelta_raw_str: (str, None)) -> (datetime.timedelta, None):
    if timedelta_raw_str is not None:
        return parse_to_timedelta(timedelta_raw_str)
    else:
        return None


def convert_to_datetime_format_or_return_self(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return isodate.duration_isoformat(obj)
    else:
        return obj
