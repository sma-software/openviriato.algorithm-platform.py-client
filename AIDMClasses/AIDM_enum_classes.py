from enum import Enum


class StopStatus(Enum):
    commercialStop = 0
    operationalStop = 1
    passing = 2


class StationEntryOrExit(Enum):
    entry = 0
    exit = 1
