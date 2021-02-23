from enum import Enum, unique


@unique
class StopStatus(Enum):
    commercial_stop = "commercialStop"
    operational_stop = "operationalStop"
    passing = "passing"


@unique
class StationEntryOrExit(Enum):
    entry = "entry"
    exit = "exit"
