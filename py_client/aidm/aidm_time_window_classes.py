import datetime


class TimeWindow:
    __from_time: datetime.datetime
    __to_time: datetime.datetime

    def __init__(self, from_time: datetime.datetime, to_time: datetime.datetime):
        self.__from_time = from_time
        self.__to_time = to_time

    @property
    def from_time(self) -> datetime.datetime:
        return self.__from_time

    @property
    def to_time(self) -> datetime.datetime:
        return self.__to_time
