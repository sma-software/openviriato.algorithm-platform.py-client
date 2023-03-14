from datetime import timedelta
from enum import unique, Enum
from typing import Optional


class _TableCell:
    __column_key: str
    __value: object

    def __init__(self, column_key: str):
        self.__column_key = column_key

    @property
    def column_key(self) -> str:
        return self.__column_key


class TableTextCell(_TableCell):
    __value: str

    def __init__(self, column_key: str, value: str):
        super().__init__(column_key)
        self.__value = value

    @property
    def value(self) -> str:
        return self.__value


class TableIntegerCell(_TableCell):
    __value: Optional[int]

    def __init__(self, column_key: str, value: Optional[int]):
        super().__init__(column_key)
        self.__value = value

    @property
    def value(self) -> Optional[int]:
        return self.__value


class TableDurationCell(_TableCell):
    __value: Optional[timedelta]

    def __init__(self, column_key: str, value: Optional[timedelta]):
        super().__init__(column_key)
        self.__value = value

    @property
    def value(self) -> Optional[timedelta]:
        return self.__value


class TableLocalDateTimeCell(_TableCell):
    __value: Optional[timedelta]

    def __init__(self, column_key: str, value: Optional[timedelta]):
        super().__init__(column_key)
        self.__value = value

    @property
    def value(self) -> Optional[timedelta]:
        return self.__value


class TableAlgorithmNodeCell(_TableCell):
    __node_id: Optional[int]

    def __init__(self, column_key: str, node_id: Optional[int]):
        super().__init__(column_key)
        self.__node_id = node_id

    @property
    def node_id(self) -> Optional[int]:
        return self.__node_id


class TableAlgorithmTrainCell(_TableCell):
    __train_id: Optional[int]

    def __init__(self, column_key: str, train_id: Optional[int]):
        super().__init__(column_key)
        self.__train_id = train_id

    @property
    def train_id(self) -> Optional[int]:
        return self.__train_id


@unique
class TableCellDataType(Enum):
    algorithm_node = "algorithmNode"
    algorithm_train = "algorithmTrain"
    duration = "duration"
    integer = "integer"
    local_date_time = "localDateTime"
    string = "string"
