from enum import Enum, unique
from typing import Optional
from py_client.aidm.aidm_update_classes import UpdateTimesTrain

@unique
class RunningTimeCalculationStatus(Enum):
    error = "error"
    ok = "ok"

class RunningTimeCalculationResult:
    __message: Optional[str]
    __update_times_train: UpdateTimesTrain
    __status: RunningTimeCalculationStatus

    def __init__(self, message: str, update_times_train: UpdateTimesTrain, status: RunningTimeCalculationStatus):
        self.__message = message
        self.__update_times_train = update_times_train
        self.__status = status

    @property
    def message(self) -> str:
        return self.__message

    @property
    def status(self) -> RunningTimeCalculationStatus:
        return self.__status

    @property
    def update_times_train(self) -> UpdateTimesTrain:
        return self.__update_times_train