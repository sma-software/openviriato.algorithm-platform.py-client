from enum import Enum
from typing import Optional
from End_to_end_tests_tool.test_case_execution.test_case import EndToEndTestCase


class TestCaseResultStatus(Enum):
    NotTested = "NotTested"
    Success = "Success"
    Error = "Error"
    Failed = "Failed"


class EndToEndTestCaseResult:
    __test_case_result_status: TestCaseResultStatus
    __error_message: str

    def __init__(self, result_status: TestCaseResultStatus, error_message: Optional[str]):
        self.__test_case_result_status = result_status
        self.__error_message = error_message

    @property
    def test_case_result_status(self) -> TestCaseResultStatus:
        return self.__test_case_result_status

    @property
    def error_message(self) -> Optional[str]:
        return self.__error_message


class ExecutedEndToEndTest:
    __executed_test_case: EndToEndTestCase
    __test_case_result: EndToEndTestCaseResult

    def __init__(self, test_case: EndToEndTestCase, test_case_result: EndToEndTestCaseResult):
        self.__executed_test_case = test_case
        self.__test_case_result = test_case_result

    @property
    def executed_test_case(self) -> EndToEndTestCase:
        return self.__executed_test_case

    @property
    def test_case_result(self) -> EndToEndTestCaseResult:
        return self.__test_case_result
