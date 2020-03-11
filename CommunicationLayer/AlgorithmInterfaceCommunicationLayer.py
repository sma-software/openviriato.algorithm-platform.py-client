import requests


def check_if_request_successful(api_response: requests.Response) -> None:
    """
    not all HTTPError Messages are completely indicative, depends on how the API is configured
    we therefore display the returned json in an additional error if it is a HTTPError
    note that the connection will remain open if no error
    """
    try:
        api_response.raise_for_status()

    except requests.HTTPError:
        # if there is an error, the algorithm platform supplies us with more information (hopefully)
        if api_response.text != '':
            rest_feedback = api_response.json()
            raise AlgorithmPlatformError(rest_feedback['statusCode'], rest_feedback['message'])

    # there was no information/json, back to the previous error
    api_response.raise_for_status()


def post_process_response(api_response) -> (dict, list, None):
    check_if_request_successful(api_response)
    return convert_body_of_response(api_response)


def convert_body_of_response(api_response) -> (dict, list, None):
    extract = None
    if api_response.text != '':
        extract = api_response.json()
    return extract


class AlgorithmPlatformError(Exception):
    def __init__(self, expression: str, message: str):
        self.expression = 'HTTPError {0}'.format(expression)
        self.message = message


class CommunicationLayer:
    base_url: str
    currentSession: requests.Session()

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.currentSession = requests.Session()

    def merge_base_url_with_request(self, request: str) -> str:
        return '{0}/{1}'.format(self.base_url, request)

    def do_get_request(self, request_call: str, request_param: dict = None) -> (dict, list):
        if request_param is None:
            request_param = {}
        complete_url = self.merge_base_url_with_request(request_call)

        api_response = self.currentSession.get(complete_url, params=request_param)

        return post_process_response(api_response)

    def do_post_request(self, request_call: str, request_body: dict = None) -> (dict, list, None):
        if request_body is None:
            request_body = {}
        complete_url = self.merge_base_url_with_request(request_call)

        api_response = self.currentSession.post(complete_url, json=request_body)

        return post_process_response(api_response)

    def do_put_request(self, request_call: str, request_body: (dict, list) = None) -> (dict, list):
        if request_body is None:
            request_body = {}
        complete_url = self.merge_base_url_with_request(request_call)

        api_response: requests.Response = self.currentSession.put(complete_url, json=request_body)

        return post_process_response(api_response)