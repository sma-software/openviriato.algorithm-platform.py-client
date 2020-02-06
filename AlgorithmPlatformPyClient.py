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
    """
    Interface to the algorithmic platform of VIRIATO. A wrapper around the REST-API.
    """
    __url_to_port: str
    __connection_behaviour: dict = dict(Connection='close')
    verbosity: int = 1

    def __init__(self, url_to_port):
        """
        to avoid side effects, it the url "protected" attribute, instantiate a new object if you want to change it
        :type url_to_port: str
        """
        assert isinstance(url_to_port, str), 'id is not a str : {0}'.format(url_to_port)
        self.__url_to_port = url_to_port

    def __check_if_request_successful(self, api_return) -> int:
        """
        not all HTTPError Messages are completely indicative, depends on how the API is configured
        we therefore display the returned json in an additional error if it is a HTTPError
        This method is mostly static, could be a function as well.
        :param api_return: the raw objected returned by the api-request
        :return: 0 if ok
        """
        try:
            api_return.raise_for_status()
        except requests.HTTPError:
            # if there is an error, the algorithm platform supplies us with more information (hopefully)
            rest_feedback = (api_return.json())
            raise AlgorithmPlatformError(rest_feedback['statusCode'], rest_feedback['message'])
        if self.verbosity > 0:
            print(api_return.url)
        return 0

    # this is just if the user wants to see the url
    def retrieve_url_to_port(self):
        """
        A getter to retrieve the url to the API
        :return: str
        """
        return self.__url_to_port

    def notify_user(self, message_level_1, message_level_2):
        """
        Allows to notify the user on the other side of the api
        :param message_level_1: str
        :param message_level_2: str
        :return: int 0 if successful
        """
        # bullet proof, check for strings to be sent:
        assert isinstance(message_level_1, str), 'message_level_1 is not a str : {0}'.format(message_level_1)
        assert isinstance(message_level_2, str), 'message_level_2 is not a str : {0}'.format(message_level_2)
        # assemble the dict
        body = dict(messageLevel1=message_level_1, messageLevel2=message_level_2)
        resp = requests.post('{0}notifications'.format(self.__url_to_port), json=body,
                             headers=self.__connection_behaviour)
        self.__check_if_request_successful(resp)
        return 0

    def show_status_message(self, short_message, long_message=None):
        """
        Notify the user of VIRIATO with information on the status bar
        :param short_message: str
        :param long_message: str, None if not required
        :return: int 0 if successful
        """
        # bullet proof, check for strings to be sent:
        assert isinstance(short_message, str), 'short_message is not a str : {0}'.format(short_message)
        if not (long_message is None):
            assert isinstance(long_message, str), 'long_message is not a str : {0}'.format(long_message)
        # not to sure about the str part!
        body = dict(shortMessage=short_message, longMessage=long_message)
        resp = requests.post('{0}status-message'.format(self.__url_to_port), json=body,
                             headers=self.__connection_behaviour)
        self.__check_if_request_successful(resp)
        return 0

    def get_neighbor_nodes(self, node_id):
        """
        Returns a list of all neighbor nodes of the given node x with nodeID == node_id, that is, all nodes y such
        that there exists at least one section track directly from x to y.
        :param node_id: int
        :return: list, containing all tracks
        """
        # bullet proofing
        assert isinstance(node_id, int), 'node_id is not an int: {0}'.format(node_id)
        # assemble and request
        api_response = requests.get('{0}neighbor-nodes/{1}'.format(self.__url_to_port, node_id),
                                    headers=self.__connection_behaviour)
        self.__check_if_request_successful(api_response)
        return api_response.json()

    def get_node(self, node_id):
        """
        Returns an IAlgorithm​Node dict for the given node_id
        :param node_id: int
        :return: dict,
        """
        # bullet proofing
        assert isinstance(node_id, int), 'node_id is not an int: {0}'.format(node_id)
        # assemble and request
        api_response = requests.get('{0}nodes/{1}'.format(self.__url_to_port, node_id),
                                    headers=self.__connection_behaviour)
        self.__check_if_request_successful(api_response)
        return api_response.json()

    def get_directed_section_tracks(self, first_node_id, second_node_id):
        """
        get all tracks in direction of the section between the two nodes. Direction given by order of the nodes
        :param first_node_id: int
        :param second_node_id: int
        :return: list, containing all tracks, empty if no tracks exist
        """
        # bullet proofing
        assert isinstance(first_node_id, int), 'first_node_id is not an int: {0}'.format(first_node_id)
        assert isinstance(second_node_id, int), 'second_node_id is not an int: {0}'.format(second_node_id)
        # assemble and request
        api_response = requests.get('{0}section-tracks-between/{1}/{2}'.format(self.__url_to_port,
                                                                               first_node_id, second_node_id),
                                    headers=self.__connection_behaviour)
        self.__check_if_request_successful(api_response)
        return api_response.json()

    def get_parallel_section_tracks(self, section_track_id):
        """
        Returns a list of all section tracks starting and ending at the same nodes as the section track with id
        section_track_id independent of the traffic-ability.
        The track with id section_track_id is included in the result.
        :param section_track_id: int
        :return: list
        """
        assert isinstance(section_track_id, int), 'section_track_id is not an int: {0}'.format(section_track_id)
        # assemble and request
        api_response = requests.get('{0}section-tracks-parallel-to/{1}'.format(self.__url_to_port,
                                                                               section_track_id),
                                    headers=self.__connection_behaviour)
        self.__check_if_request_successful(api_response)
        return api_response.json()


def __void_get_directed_section_tracks(self, first_node_id, second_node_id):
    """"""
    # bullet proofing
    assert isinstance(first_node_id, int), 'first_node_id is not an int: {0}'.format(first_node_id)
    assert isinstance(second_node_id, int), 'second_node_id is not an int: {0}'.format(second_node_id)
    # assemble parameters
    get_request_parameters = dict(firstNodeID=first_node_id, secondNodeID=second_node_id)
    api_response = requests.get('{0}assignable-station-tracks-on-train-path-node?'.format(self.__url_to_port),
                                params=get_request_parameters)
    self.__check_if_request_successful(api_response)
    # return has to be formatted! raw for now


class AlgorithmicPlatformInterfaceDebug(AlgorithmicPlatformInterface):
    """
    this class is only meant as a debug/etc, not for productive use!
    Interface to the algorithmic platform of VIRIATO. A wrapper around the REST-API.
    """

    def some_action(self):
        print('nothing to see here, i am a spaceholder')

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


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class AlgorithmPlatformError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = 'HTTPError {0}'.format(expression)
        self.message = message
