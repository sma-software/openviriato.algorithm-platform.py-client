from typing import Optional, List


class Result:
    __result_value: Optional[List[str]]
    __error_message: Optional[str]

    def __init__(self, result_value: Optional[List[str]], error_message):
        self.__result_value = result_value
        self.__error_message = error_message

    @property
    def is_success(self) -> bool:
        return self.__error_message is None

    @property
    def error_message(self) -> str:
        return self.__error_message

    @property
    def result_value(self) -> Optional[List[str]]:
        return self.__result_value


def from_result(result_value: Optional[List[str]]) -> Result:
    return Result(result_value=result_value, error_message=None)


def from_error(error_message: str) -> Result:
    return Result(result_value=None, error_message=error_message)
