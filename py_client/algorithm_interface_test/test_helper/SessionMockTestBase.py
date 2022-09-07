class SessionMockTestBase:
    _last_request: str
    _last_parameters: dict
    _last_body: dict

    def __init__(self):
        self._last_request = str()
        self._last_parameters = dict()
        self._last_body = dict()

    @property
    def last_request(self) -> str:
        return self._last_request

    @property
    def last_parameters(self) -> dict:
        return self._last_parameters

    @property
    def last_body(self) -> dict:
        return self._last_body

    def close(self):
        pass


def get_api_url():
    url_str = "http://localhost:8080"
    return url_str
