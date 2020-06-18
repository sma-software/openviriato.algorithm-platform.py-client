from typing import Union


class EndToEndTestCase:
    _name_of_test_case: str
    _name_of_method_to_test: str
    _parameters_for_method_to_test: list
    _expected_response_as_json: Union[list, dict]

    def __init__(self,
                 name_of_test_case: str,
                 name_of_method_to_test: str,
                 parameters_for_method_to_test,
                 expected_response_as_json):
        self._name_of_test_case = name_of_test_case
        self._name_of_method_to_test = name_of_method_to_test
        self._parameters_for_method_to_test = parameters_for_method_to_test
        self._expected_response_as_json = expected_response_as_json

    @property
    def test_case_name(self) -> str:
        return self._name_of_test_case

    @property
    def name_of_method_to_test(self) -> str:
        return self._name_of_method_to_test

    @property
    def parameters_for_method_to_test(self) -> list:
        return self._parameters_for_method_to_test

    @property
    def expected_response_as_json(self) -> Union[list, dict]:
        return self._expected_response_as_json
