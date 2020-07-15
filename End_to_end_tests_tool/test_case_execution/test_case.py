from typing import Union


class EndToEndTestCase:
    _name_of_method_to_test: str
    _arguments_for_py_client_method: list
    _expected_response_as_json: Union[list, dict]

    def __init__(self,
                 name_of_method_to_test: str,
                 py_client_parameters: list,
                 expected_response_as_json: dict):
        self._name_of_method_to_test = name_of_method_to_test
        self._arguments_for_py_client_method = py_client_parameters
        self._expected_response_as_json = expected_response_as_json

    @property
    def name_of_method_to_test(self) -> str:
        return self._name_of_method_to_test

    @property
    def arguments_for_py_client_method(self) -> list:
        return self._arguments_for_py_client_method

    @property
    def expected_response_as_json(self) -> Union[list, dict]:
        return self._expected_response_as_json
