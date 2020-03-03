class SessionMockTestBase:
    __last_body: dict
    __last_request: str

    def __init__(self):
        # print('created a Mocked session')
        self.__last_request = str()
        self.__last_body = dict()

    def close(self):
        # #print('closed a Mocked session')
        self


def get_api_url():
    url_str = 'http://localhost:8080'
    return url_str
