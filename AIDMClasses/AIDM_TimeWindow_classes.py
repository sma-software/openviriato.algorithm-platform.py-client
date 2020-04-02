import datetime


class TimeWindow:
    __FromTime: datetime.datetime
    __ToTime: datetime.datetime

    def __init__(self, FromTime: datetime.datetime, ToTime: datetime.datetime):
        self.__FromTime = FromTime
        self.__ToTime = ToTime

    @property
    def FromTime(self) -> datetime.datetime:
        return self.__FromTime

    @property
    def ToTime(self) -> datetime.datetime:
        return self.__ToTime