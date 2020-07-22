class SessionMockTestBase:
    __last_body: dict
    __last_request: str

    def __init__(self):
        self.__last_request = str()
        self.__last_body = dict()

    def close(self):
        pass


def get_api_url():
    url_str = 'http://localhost:8080'
    return url_str
