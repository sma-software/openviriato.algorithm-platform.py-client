from enum import Enum
from typing import Optional


class TestCaseResultStatus(Enum):
    NotTested = "NotTested"
    Success = "Success"
    Error = "Error"
    Failed = "Failed"


class EndToEndTestCaseResult:
    __test_case_result_status: TestCaseResultStatus
    __error_message: Optional[str]
    __invoked_method_name: str
    __applied_arguments: list

    def __init__(
            self,
            result_status: TestCaseResultStatus,
            error_message: Optional[str],
            invoked_method_name: str,
            applied_arguments: list):
        self.__test_case_result_status = result_status
        self.__error_message = error_message
        self.__applied_arguments = applied_arguments
        self.__invoked_method_name = invoked_method_name

    @property
    def test_case_result_status(self) -> TestCaseResultStatus:
        return self.__test_case_result_status

    @property
    def error_message(self) -> Optional[str]:
        return self.__error_message

    @property
    def invoked_method_name(self) -> str:
        return self.__invoked_method_name

    @property
    def applied_arguments(self) -> list:
        return self.__applied_arguments
