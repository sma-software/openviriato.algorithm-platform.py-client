from enum import Enum
from typing import Optional


class TestCaseResultStatus(Enum):
    NotTested = "NotTested"
    Success = "Success"
    Error = "Error"
    Failed = "Failed"


class HeadlessTestCaseResult:
    _test_case_result_status: TestCaseResultStatus = TestCaseResultStatus["NotTested"]
    _error_message: str = 'This test has not been Performed'

    def __init__(self, result_status: TestCaseResultStatus, error_message: Optional[str]):
        self._test_case_result_status = result_status
        self._error_message = error_message

    @property
    def test_case_result_status(self) -> TestCaseResultStatus:
        return self._test_case_result_status

    @property
    def error_message(self) -> Optional[str]:
        return self._error_message
