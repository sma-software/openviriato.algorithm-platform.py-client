from typing import Union, Optional

Primitive = Union[int, str, bool, Optional[int], Optional[str], Optional[bool]]

def is_primitive(value: object):
    return value in Primitive.__args__
