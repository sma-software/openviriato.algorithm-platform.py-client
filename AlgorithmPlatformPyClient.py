"""
This is the module intended to act as an interface to the algorithmic platform of VIRIATO
It wraps around the REST-API to enhance the usability
It consists on one hand of the interface as well as the various requests.
"""

__all__ = ['AlgorithmicPlatformInterface']
__version__ = '0.0.1'
__author__ = 'Florian Fuchs'

import requests
import AlgorithmClasses


class AlgorithmicPlatformInterface:
    """
    Interface to the algorithmic platform of VIRIATO. A wrapper around the REST-API.
    """
    __base_url: str
    __session: requests.Session()

    def __init__(self, base_url: str):
        """
        to avoid side effects, it the url "protected" attribute, instantiate a new object if you want to change it
        :type url_to_port: str
        """
        self.__verify_parameter_is_str(base_url, 'base_url', '__init__')
        self.__base_url = base_url
        self.__session = requests.Session()
        print('init')
        # .__init_interface(base_url)

    def __enter__(self, base_url: str = 11):
        # to be used in with context
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        # try to close the connection here
        self.__session.close()
        print('destructor-like exit ')
        # always close session when destruct

    def __check_if_request_successful(self, api_return: requests.Response):
        """
        not all HTTPError Messages are completely indicative, depends on how the API is configured
        we therefore display the returned json in an additional error if it is a HTTPError
        This method is mostly static, could be a function as well.
        :param api_return: the raw objected returned by the api-request
        """
        try:
            api_return.raise_for_status()
        except requests.HTTPError:

            # if there is an error, the algorithm platform supplies us with more information (hopefully)
            rest_feedback = (api_return.json())
            raise AlgorithmPlatformError(rest_feedback['statusCode'], rest_feedback['message'])

    def __assemble_url_and_request(self, request: str) -> str:
        return '{0}/{1}'.format(self.__base_url, request)

    def __verify_input(self, received_object: object, required_object: object, object_name: str, method_name: str):
        assert isinstance(received_object, required_object), \
            "in method {0}, \n the parameter {0} is required to be of type {1} \n " \
            "but it was a instead: {2}".format(method_name, object_name, required_object.__name__,
                                               received_object.__class__)

    def __verify_parameter_is_str(self, received_object: object, object_name: str, method_name: str):
        assert isinstance(received_object, str), \
            "in method {0}, \n the parameter {0} is required to be of type str \n " \
            "but it was a instead: {2}".format(method_name, object_name, received_object.__class__)

    def __verify_parameter_is_int(self, received_object: object, object_name: str, method_name: str):
        assert isinstance(received_object, int), \
            "in method {0}, \n the parameter {0} is required to be of type int \n " \
            "but it was a instead: {2}".format(method_name, object_name, received_object.__class__)

    # this is just if the user wants to see the url
    def get_url_to_port(self) -> str:
        """
        A getter to retrieve the url to the API
        :return: str
        """
        return self.__base_url

    def notify_user(self, message_level_1: str, message_level_2: str):
        """
        Allows to notify the user on the other side of the api
        :param message_level_1: str
        :param message_level_2: str
        """
        self.__verify_parameter_is_str(message_level_1, 'message_level_1', 'notify_user')
        self.__verify_parameter_is_str(message_level_2, 'message_level_2', 'notify_user')
        # assemble the dict
        body = dict(messageLevel1=message_level_1, messageLevel2=message_level_2)
        complete_url = self.__assemble_url_and_request('notifications')
        api_response = self.__session.post(complete_url, json=body)
        self.__check_if_request_successful(api_response)

    def show_status_message(self, short_message: str, long_message=None):
        """
        Notify the user of VIRIATO with information on the status bar
        :param short_message: str
        :param long_message: str, None if not required
        """
        self.__verify_parameter_is_str(short_message, 'short_message', 'show_status_message')
        if not (long_message is None):
            self.__verify_parameter_is_str(short_message, 'long_message', 'show_status_message')
        body = dict(shortMessage=short_message, longMessage=long_message)
        complete_url = self.__assemble_url_and_request('status-message')
        api_response = self.__session.post(complete_url, json=body)
        self.__check_if_request_successful(api_response)

    def get_neighbor_nodes(self, node_id: int) -> tuple:
        """
        Returns a list of all neighbor nodes of the given node x with nodeID == node_id, that is, all nodes y such
        that there exists at least one section track directly from x to y.
        :param node_id: int
        :return: list, containing all tracks
        """
        self.__verify_parameter_is_int(node_id, 'node_id', 'get_neighbor_nodes')
        url_tail = 'neighbor-nodes/{0}'.format(node_id)
        complete_url = self.__assemble_url_and_request(url_tail)
        api_response = self.__session.get(complete_url)
        self.__check_if_request_successful(api_response)
        return api_response.json()

    def get_node(self, node_id: int) -> AlgorithmClasses.AlgorithmNode:
        """
        Returns an IAlgorithm​Node dict for the given node_id
        :param node_id: int
        :return: dict,
        """
        self.__verify_parameter_is_int(node_id, 'node_id', 'get_node')
        url_tail = 'nodes/{0}'.format(node_id)
        complete_url = self.__assemble_url_and_request(url_tail)
        api_response = self.__session.get(complete_url)
        self.__check_if_request_successful(api_response)
        return api_response.json()

    def get_directed_section_tracks(self, first_node_id: int, second_node_id: int) -> tuple:
        """
        get all tracks in direction of the section between the two nodes. Direction given by order of the nodes
        :param first_node_id: int
        :param second_node_id: int
        :return: tuple, containing all tracks, empty if no tracks exist
        """
        self.__verify_parameter_is_int(first_node_id, 'first_node_id', 'get_directed_section_tracks')
        self.__verify_parameter_is_int(second_node_id, 'second_node_id', 'get_directed_section_tracks')
        # assemble and request
        url_tail = 'section-tracks-between/{0}/{1}'.format(first_node_id, second_node_id)
        complete_url = self.__assemble_url_and_request(url_tail)
        api_response = self.__session.get(complete_url)
        self.__check_if_request_successful(api_response)
        return api_response.json()

    def get_parallel_section_tracks(self, section_track_id: int) -> tuple:
        """
        Returns a list of all section tracks starting and ending at the same nodes as the section track with id
        section_track_id independent of the traffic-ability.
        The track with id section_track_id is included in the result.
        :param section_track_id: int
        :return: tuple
        """
        self.__verify_parameter_is_int(section_track_id, 'section_track_id', 'get_parallel_section_tracks')
        url_tail = 'section-tracks-parallel-to/{0}'.format(section_track_id)
        complete_url = self.__assemble_url_and_request(url_tail)
        api_response = self.__session.get(complete_url)
        self.__check_if_request_successful(api_response)
        return api_response.json()


class AlgorithmicPlatformInterfaceDebug(AlgorithmicPlatformInterface):
    """
    this class is only meant as a debug/etc, not for productive use!
    Interface to the algorithmic platform of VIRIATO. A wrapper around the REST-API.
    """

    def some_action(self):
        print('nothing to see here, i am a placeholder')

    def do_request(self, request_str, request_type, request_body=None, params_dict=None):
        rest_str = self.__base_url + request_str
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
