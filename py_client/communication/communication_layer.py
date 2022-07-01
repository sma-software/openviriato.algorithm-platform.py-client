import requests
from requests import Session
import http
from py_client.communication.response_processing import extract_json_if_possible


class CommunicationLayer:
    base_url: str
    currentSession: Session

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.currentSession = requests.Session()

    def merge_base_url_with_request(self, request: str) -> str:
        return '{0}/{1}'.format(self.base_url, request)

    def do_get_request_without_body(self, request_call: str, query_parameters: dict = None) -> (dict, list):
        if query_parameters is None:
            query_parameters = {}
        complete_url = self.merge_base_url_with_request(request_call)

        api_response = self.currentSession.get(complete_url, params=query_parameters)

        return extract_json_if_possible(api_response)

    def do_get_request_with_body(self, request_call: str, body: dict, query_parameters: dict = None) -> (dict, list):
        if query_parameters is None:
            query_parameters = {}

        complete_url = self.merge_base_url_with_request(request_call)

        api_response = self.currentSession.get(complete_url, params=query_parameters, json=body)

        return extract_json_if_possible(api_response)

    def do_post_request(self, request_call: str, request_body: dict = None) -> (dict, list, None):
        if request_body is None:
            request_body = {}
        complete_url = self.merge_base_url_with_request(request_call)

        api_response = self.currentSession.post(complete_url, json=request_body)

        return extract_json_if_possible(api_response)

    def do_put_request(self, request_call: str, request_body: (dict, list) = None) -> (dict, list):
        if request_body is None:
            request_body = {}
        complete_url = self.merge_base_url_with_request(request_call)

        api_response: requests.Response = self.currentSession.put(complete_url, json=request_body)

        return extract_json_if_possible(api_response)

    def do_delete_request(self, request_call: str, request_body: (dict, list) = None) -> (dict, list):
        if request_body is None:
            request_body = {}
        complete_url = self.merge_base_url_with_request(request_call)

        api_response: requests.Response = self.currentSession.delete(complete_url, json=request_body)

        return extract_json_if_possible(api_response)
