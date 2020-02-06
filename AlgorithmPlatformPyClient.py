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
        assert isinstance(url_to_port, str), 'id is not a str : {0}'.format(url_to_port)
        self.__url_to_port = url_to_port

    # helper (private) to check if there is an error --> exception is here
    def __check_status(self, api_return):
        api_return.raise_for_status()
        if self.verbosity > 0:
            print(api_return.url)

    # this is just if the user wants to see the url
    def retrieve_url_to_port(self):
        return self.__url_to_port

    def notify_user(self, message_level_1, message_level_2):
        # bullet proof, check for strings to be sent:
        assert isinstance(message_level_1, str), 'message_level_1 is not a str : {0}'.format(message_level_1)
        assert isinstance(message_level_2, str), 'message_level_2 is not a str : {0}'.format(message_level_2)
        # assemble the dict
        body = dict(messageLevel1=message_level_1, messageLevel2=message_level_2)
        resp = requests.post('{0}notifications'.format(self.__url_to_port), json=body)
        self.__check_status(resp)

    def show_status_message(self, short_message, long_message=None):
        # bullet proof, check for strings to be sent:
        assert isinstance(short_message, str), 'short_message is not a str : {0}'.format(short_message)
        if not (long_message is None):
            assert isinstance(long_message, str), 'long_message is not a str : {0}'.format(long_message)
        # not to sure about the str part!
        body = dict(shortMessage=short_message, longMessage=long_message)
        resp = requests.post('{0}status-message'.format(self.__url_to_port), json=body)
        self.__check_status(resp)

    def get_directed_section_tracks(self, first_node_id, second_node_id):
        # bullet proofing
        assert isinstance(first_node_id, int), 'first_node_id is not an int: {0}'.format(first_node_id)
        assert isinstance(second_node_id, int), 'second_node_id is not an int: {0}'.format(second_node_id)
        # insert method later pls, check assertion first
        get_request_str = 'assignable-station-tracks-on-train-path-node?'
        get_request_parameters = dict(firstNodeID=first_node_id, secondNodeID=second_node_id)
        api_response = requests.get('{0}assignable-station-tracks-on-train-path-node?'.format(self.__url_to_port),
                                    json=get_request_parameters)



# this class is only ment as a debug/etc, not for productive use!
class AlgorithmicPlatformInterfaceEnhanced(AlgorithmicPlatformInterface):

    def some_action(self):
        print('nothing to do here, i am a spaceholder')

    def do_request(self, request_str, request_type, request_body=None, params_dict=None):
        rest_str = self.__url_to_port + request_str
        if request_type == 'GET':
            api_response = requests.get(rest_str, params=params_dict)
        elif request_type == 'POST':
            api_response = requests.post(rest_str, json=request_body)
        elif request_type == 'PUT':
            api_response = requests.put(rest_str, json=request_body)
        else:
            print('undefined request type, must be GET, POST, PUT')
            raise
        # if there is any error, we raise it here
        api_response.raise_for_status()
        return api_response
