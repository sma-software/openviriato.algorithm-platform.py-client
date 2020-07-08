from enum import Enum


class StopStatus(Enum):
    commercial_stop = 0
    operational_stop = 1
    passing = 2


class StationEntryOrExit(Enum):
    entry = 0
    exit = 1
