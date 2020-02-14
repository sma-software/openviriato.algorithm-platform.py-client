import json


# This method will be used by the mock to replace requests.get/post/put
def mocked_requests_response(json_string: str, status_code: int = 200):
    class MockResponse:
        def __init__(self, json_loads_string: str, http_status: int = 200):
            self.json_string = json_loads_string
            self.status_code = http_status

        def raise_for_status(self) -> None:
            if not (self.status_code == 200):
                raise NotImplementedError(self.status_code)

        def json(self) -> dict:
            return json.loads(self.json_string)

    return MockResponse(json_string, status_code)


class MockedRequestsSessionBaseClass:

    def __init__(self):
        print('created a Mocked session')

    def close(self):
        print('closed a Mocked session')