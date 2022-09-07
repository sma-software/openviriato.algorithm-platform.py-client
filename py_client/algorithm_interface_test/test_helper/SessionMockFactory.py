import json


def create_response_mock(json_string: str, status_code: int = 200):
    class ResponseMock:
        def __init__(self, json_loads_string: str, http_status: int = 200):
            self.text = json_loads_string
            self.status_code = http_status

        def raise_for_status(self) -> None:
            if not (self.status_code == 200):
                raise NotImplementedError(self.status_code)

        def json(self) -> dict:
            return json.loads(self.text)

    return ResponseMock(json_string, status_code)
