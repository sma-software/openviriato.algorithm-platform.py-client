import requests


def raise_if_unsuccessful_response_code(api_response: requests.Response) -> None:
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


def extract_json_if_possible(api_response) -> (dict, list, None):
    raise_if_unsuccessful_response_code(api_response)
    return extract_json_or_none(api_response)


def extract_json_or_none(api_response) -> (dict, list, None):
    extract = None
    if api_response.text != '':
        extract = api_response.json()
    return extract


class AlgorithmPlatformError(Exception):
    def __init__(self, expression: str, message: str):
        self.expression = 'HTTPError {0}'.format(expression)
        self.message = message