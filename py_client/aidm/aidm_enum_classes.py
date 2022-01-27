from enum import Enum, unique
from typing import TypeVar


@unique
class StopStatus(Enum):
    commercial_stop = "commercialStop"
    operational_stop = "operationalStop"
    passing = "passing"


@unique
class StationEntryOrExit(Enum):
    entry = "entry"
    exit = "exit"


EnumType = TypeVar("EnumType", bound=Enum)