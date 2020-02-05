"""
This is the module intended to act as an interface to the algorithmic platform of VIRIATO
It wraps around the REST-API to enhance the usability
It consists on one hand of the interface as well as the various requests.
"""

__all__ = ['AlgorithmicPlatformInterface']
__version__ = '0.0.1'
__author__ = 'Florian Fuchs'

import requests


class AlgorithmicPlatformInterface:
    __url_to_port: str
    verbosity: int = 1

    def __init__(self, url_to_port):
        """
        :type url_to_port: str
        """
        # to avoid side effects, it is a protected attribute, instantiate a new object if you want to change it
        assert isinstance(url_to_port, str), "id is not a str : {}".format(url_to_port)
        self.__url_to_port = url_to_port

    # helper (private) to check if there is an error --> exception is here
    def __check_status(self, api_return):
        api_return.raise_for_status()
        if self.verbosity > 0:
            print(api_return.url)

    # this is just if the user wants to see the url
    def retrieve_url_to_port(self):
        return self.__url_to_port

    # classic hello world example
    def notify_user(self, message_level_1, message_level_2):
        # not to sure about the str part!
        body = dict(messageLevel1=str(message_level_1), messageLevel2=str(message_level_2))
        resp = requests.post(self.__url_to_port + "notifications", json=body)
        self.__check_status(resp)

    # classic hello world example
    def show_status_message(self, short_message, long_message = None):
            # not to sure about the str part!
            body = dict(shortMessage=str(short_message), longMessage =str(long_message))
            resp = requests.post(self.__url_to_port + "status-message", json=body)
            self.__check_status(resp)



    def some_action(self):
        print('nothing to do here, i am a spaceholder')

    def do_request(self, request_str, request_type, request_body=None, params_dict=None):
        rest_str = self.__url_to_port + request_str
        if request_type == 'GET':
            resp = requests.get(rest_str, params=params_dict)
        elif request_type == 'POST':
            resp = requests.post(rest_str, json=request_body)
        elif request_type == 'PUT':
            resp = requests.put(rest_str, json=request_body)
        else:
            print('undefined request type, must be GET, POST, PUT')
            raise
        # if there is any error, we raise it here
        resp.raise_for_status()
        return resp
