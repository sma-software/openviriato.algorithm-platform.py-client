import requests


def raise_if_unsuccessful_response_code(api_response: requests.Response) -> None:
    try:
        api_response.raise_for_status()

    except requests.HTTPError:
        if api_response.text != "":
            algorithm_platform_error_information = api_response.json()
            raise AlgorithmPlatformHTTPError(algorithm_platform_error_information["statusCode"], algorithm_platform_error_information["message"])
        else:
            api_response.raise_for_status()


def extract_json_if_possible(api_response) -> (dict, list, None):
    raise_if_unsuccessful_response_code(api_response)
    return extract_json_or_none(api_response)


def extract_json_or_none(api_response) -> (dict, list, None):
    if api_response.text != "":
        return api_response.json()
    else:
        return None


class AlgorithmPlatformHTTPError(Exception):
    def __init__(self, status_code: str, message: str):
        self.status_code = "HTTPError {0}".format(status_code)
        self.message = message


class AlgorithmPlatformConversionError(Exception):
    def __init__(self, message: str, wrapped_exception: Exception):
        self.wrapped_exception = wrapped_exception
        self.message = message
