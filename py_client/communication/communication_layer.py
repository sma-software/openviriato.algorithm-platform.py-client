import requests
from requests import Session
from http import client
from py_client.communication.response_processing import extract_json_if_possible
import logging
import json
import os
from datetime import datetime


class DebugAdapter(requests.adapters.HTTPAdapter):
    def send(self, request, **kwargs):
        logging.debug(f"Request URL: {request.url}")
        logging.debug(f"Request Headers: {request.headers}")
        if request.body:
            try:
                body = json.loads(request.body)
                logging.debug(f"Request Body: {json.dumps(body, indent=2)}")
            except:
                logging.debug(f"Request Body: {request.body}")

        response = super().send(request, **kwargs)

        logging.debug(f"Response Status: {response.status_code}")
        logging.debug(f"Response Headers: {response.headers}")
        try:
            body = response.json()
            logging.debug(f"Response Body: {json.dumps(body, indent=2)}")
        except:
            logging.debug(f"Response Body: {response.text}")

        return response


class CommunicationLayer:
    base_url: str
    currentSession: Session

    def __init__(self, base_url: str, log_file: str = None):
        client.HTTPConnection.debuglevel = 2
        self.base_url = base_url
        self.currentSession = requests.Session()
        if log_file:
            print("http logging is turned on. Will log to {}".format(os.path.abspath(log_file)))
            self.currentSession.mount("http://", DebugAdapter())
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler(log_file)])
        else:
            print("http logging is turned off. Activate by handing over a log file path to the AlgorithmInterface constructor.")

    def merge_base_url_with_request(self, request: str) -> str:
        return "{0}/{1}".format(self.base_url, request)

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
