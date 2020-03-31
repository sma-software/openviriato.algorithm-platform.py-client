import datetime
import enum

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


def check_and_format_any_datetime_to_iso_str(obj):
    if isinstance(obj, datetime.datetime):
        obj = obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        obj = isodate.duration_isoformat(obj)
    return obj


def check_and_format_any_enum_to_str(obj):
    if isinstance(obj, enum.Enum):
        obj = obj.name
    return obj
