import requests


def raise_if_unsuccessful_response_code(api_response: requests.Response) -> None:
    try:
        api_response.raise_for_status()

    except requests.HTTPError:
        if api_response.text != '':
            algorithm_platform_error_information = api_response.json()
            raise AlgorithmPlatformError(
                algorithm_platform_error_information['statusCode'],
                algorithm_platform_error_information['message']
            )
        else:
            api_response.raise_for_status()


def extract_json_if_possible(api_response) -> (dict, list, None):
    raise_if_unsuccessful_response_code(api_response)
    return extract_json_or_none(api_response)


def extract_json_or_none(api_response) -> (dict, list, None):
    if api_response.text != '':
        return api_response.json()
    else:
        return None


class AlgorithmPlatformError(Exception):
    def __init__(self, expression: str, message: str):
        self.expression = 'HTTPError {0}'.format(expression)
        self.message = message
