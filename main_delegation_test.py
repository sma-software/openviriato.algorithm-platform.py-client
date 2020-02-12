import requests
import json
import AlgorithmClasses
import AlgorithmTypeCheck


def custom_dir(c, add): return dir(type(c)) + list(c.__dict__.keys()) + add


class GetAttr:
    """Base class for attr accesses in `self._xtra` passed down to `self.default`"""

    @property
    def _xtra(self): return [o for o in dir(self.default) if not o.startswith('_')]

    def __getattr__(self, k):
        if k in self._xtra: return getattr(self.default, k)
        raise AttributeError(k)

    def __dir__(self): return custom_dir(self, self._xtra)


class AlgorithmicPlatformInterface(GetAttr):
    """
    Interface to the algorithmic platform of VIRIATO. A wrapper around the REST-API.
    Supports and is intended to be used in with statements
    """
    __base_url: str
    __currentSession: requests.Session()

    def __init__(self, base_url: str):
        AlgorithmTypeCheck.assert_parameter_is_str(base_url, 'base_url', '__init__')
        self.__base_url = base_url
        self.__currentSession = requests.Session()
        self.__CommLayer = AlgorithmicPlatformCommuncationLayer()

    def __enter__(self):
        return self  # to be used in with statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__currentSession.close()


    @property
    def base_url(self) -> str:
        return self.__base_url


class AlgorithmicPlatformCommuncationLayer:

    def __init__(self):
        print()

    # move everything with communication in an own layer
    def __merge_base_url_with_request(self, request: str) -> str:
        return '{0}/{1}'.format(self.__base_url, request)

    def __do_get_request(self, request_call: str, request_param: dict = None) -> requests.Response:
        if request_param is None:
            request_param = {}
        complete_url = self.__merge_base_url_with_request(request_call)
        api_response = self.__currentSession.get(complete_url, params=request_param)
        AlgorithmTypeCheck.check_if_request_successful(api_response)
        return api_response

    def __do_post_request(self, request_call: str, request_body: dict = None) -> requests.Response:
        if request_body is None:
            request_body = {}
        complete_url = self.__merge_base_url_with_request(request_call)
        api_response = self.__currentSession.post(complete_url, json=request_body)
        AlgorithmTypeCheck.check_if_request_successful(api_response)
        return api_response

    def __do_put_request(self, request_call: str, request_body: dict = None) -> requests.Response:
        if request_body is None:
            request_body = {}
        complete_url = self.__merge_base_url_with_request(request_call)
        api_response = self.__currentSession.put(complete_url, json=request_body)
        AlgorithmTypeCheck.check_if_request_successful(api_response)
        return api_response


if __name__ == '__main__':
    IF = AlgorithmicPlatformInterface(r'http://localhost:8080')
    IF.__