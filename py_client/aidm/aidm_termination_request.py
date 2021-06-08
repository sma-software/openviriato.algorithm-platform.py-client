from abc import ABC
from datetime import datetime
from enum import unique, Enum
from typing import Optional


@unique
class SignalType(Enum):
    termination = "Termination"


class ABCSignal(ABC):
    pass


class TerminationRequest(ABCSignal):
    __termination_requested_timestamp: Optional[datetime]

    def __init__(self, termination_requested_timestamp: Optional[datetime]) -> None:
        self.__termination_requested_timestamp = termination_requested_timestamp

    @property
    def termination_requested_timestamp(self) -> Optional[datetime]:
        return self.__termination_requested_timestamp
