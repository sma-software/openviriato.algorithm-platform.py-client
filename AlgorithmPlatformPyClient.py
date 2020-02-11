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
import AlgorithmStatic


def initialise_algorithm_node_from_dict(Node_as_dict: dict) -> AlgorithmClasses.AlgorithmNode:
    return AlgorithmClasses.AlgorithmNode(node_id=Node_as_dict['ID'],
                                          code_string=Node_as_dict['Code'],
                                          node_tracks=Node_as_dict['NodeTracks'],
                                          debug_string=Node_as_dict['DebugString'])


def initialise_algorithm_node_list(list_of_nodes_as_dict: list) -> list:
    node_list = list()
    for Node_as_dict in list_of_nodes_as_dict:
        node_list.append(initialise_algorithm_node_from_dict(Node_as_dict))
    return node_list


def initialise_algorithm_section_track_from_dict(section_track_as_dict: dict) -> AlgorithmClasses.AlgorithmSectionTrack:
    return AlgorithmClasses.AlgorithmSectionTrack(section_id=section_track_as_dict['ID'],
                                                  code_string=section_track_as_dict['Code'],
                                                  section_code=section_track_as_dict['SectionCode'],
                                                  debug_string=section_track_as_dict['DebugString'],
                                                  section_weight=section_track_as_dict['Weight'])


def initialise_algorithm_section_track_list(list_of_sections_dict: list) -> list:
    section_track_list = list()
    for section_as_dict in list_of_sections_dict:
        section_track_list.append(initialise_algorithm_section_track_from_dict(section_as_dict))
    return section_track_list


class AlgorithmicPlatformInterface:
    """
    Interface to the algorithmic platform of VIRIATO. A wrapper around the REST-API.
    Supports and is intended to be used in with statements
    """
    __base_url: str
    __currentSession: requests.Session()

    def __init__(self, base_url: str):
        """
        to avoid side effects, it the url "protected" attribute, instantiate a new object if you want to change it
        :type base_url: str
        """
        AlgorithmStatic.assert_parameter_is_str(base_url, 'base_url', '__init__')
        self.__base_url = base_url
        self.__currentSession = requests.Session()

    def __enter__(self):
        return self  # to be used in with context

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__currentSession.close()  # close the connection here

    def __merge_base_url_with_request(self, request: str) -> str:
        return '{0}/{1}'.format(self.__base_url, request)

    @property
    def base_url(self) -> str:
        return self.__base_url

    def notify_user(self, message_level_1: str, message_level_2: str) -> None:
        """
        Allows to notify the user on the other side of the api
        :param message_level_1: str
        :param message_level_2: str
        """
        AlgorithmStatic.assert_parameter_is_str(message_level_1, 'message_level_1', 'notify_user')
        AlgorithmStatic.assert_parameter_is_str(message_level_2, 'message_level_2', 'notify_user')
        request_body = dict(messageLevel1=message_level_1, messageLevel2=message_level_2)
        complete_url = self.__merge_base_url_with_request('notifications')
        api_response = self.__currentSession.post(complete_url, json=request_body)
        AlgorithmStatic.check_if_request_successful(api_response)

    def show_status_message(self, short_message: str, long_message=None) -> None:
        """
        Notify the user of VIRIATO with information on the status bar
        :param short_message: str
        :param long_message: str, None if not required
        """
        AlgorithmStatic.assert_parameter_is_str(short_message, 'short_message', 'show_status_message')
        if not (long_message is None):
            AlgorithmStatic.assert_parameter_is_str(short_message, 'long_message', 'show_status_message')
        request_body = dict(shortMessage=short_message, longMessage=long_message)
        complete_url = self.__merge_base_url_with_request('status-message')
        api_response = self.__currentSession.post(complete_url, json=request_body)
        AlgorithmStatic.check_if_request_successful(api_response)

    def get_neighbor_nodes(self, node_id: int) -> tuple:
        """
        Returns a list of all neighbor nodes of the given node x with nodeID == node_id, that is, all nodes y such
        that there exists at least one section track directly from x to y.
        :param node_id: int
        :return: list, containing all tracks
        """
        AlgorithmStatic.assert_parameter_is_int(node_id, 'node_id', 'get_neighbor_nodes')
        url_tail = 'neighbor-nodes/{0}'.format(node_id)
        complete_url = self.__merge_base_url_with_request(url_tail)
        api_response = self.__currentSession.get(complete_url)
        AlgorithmStatic.check_if_request_successful(api_response)
        return initialise_algorithm_node_list(api_response.json())

    def get_node(self, node_id: int) -> AlgorithmClasses.AlgorithmNode:
        """
        Returns an IAlgorithm​Node dict for the given node_id
        :param node_id: int
        :return: dict,
        """
        AlgorithmStatic.assert_parameter_is_int(node_id, 'node_id', 'get_node')
        url_tail = 'nodes/{0}'.format(node_id)
        complete_url = self.__merge_base_url_with_request(url_tail)
        api_response = self.__currentSession.get(complete_url)
        AlgorithmStatic.check_if_request_successful(api_response)
        return initialise_algorithm_node_from_dict(api_response.json())

    def get_directed_section_tracks(self, first_node_id: int, second_node_id: int) -> tuple:
        """
        get all tracks in direction of the section between the two nodes. Direction given by order of the nodes
        :param first_node_id: int
        :param second_node_id: int
        :return: tuple, containing all tracks, empty if no tracks exist
        """
        AlgorithmStatic.assert_parameter_is_int(first_node_id, 'first_node_id', 'get_directed_section_tracks')
        AlgorithmStatic.assert_parameter_is_int(second_node_id, 'second_node_id', 'get_directed_section_tracks')
        # assemble and request
        url_tail = 'section-tracks-between/{0}/{1}'.format(first_node_id, second_node_id)
        complete_url = self.__merge_base_url_with_request(url_tail)
        api_response = self.__currentSession.get(complete_url)
        AlgorithmStatic.check_if_request_successful(api_response)
        return initialise_algorithm_section_track_list(api_response.json())

    def get_parallel_section_tracks(self, section_track_id: int) -> tuple:
        """
        Returns a list of all section tracks starting and ending at the same nodes as the section track with id
        section_track_id independent of the traffic-ability.
        The track with id section_track_id is included in the result.
        :param section_track_id: int
        :return: tuple
        """
        AlgorithmStatic.assert_parameter_is_int(section_track_id, 'section_track_id', 'get_parallel_section_tracks')
        url_tail = 'section-tracks-parallel-to/{0}'.format(section_track_id)
        complete_url = self.__merge_base_url_with_request(url_tail)
        api_response = self.__currentSession.get(complete_url)
        AlgorithmStatic.check_if_request_successful(api_response)
        print(api_response.json())
        raise NotImplementedError
        return api_response.json()


class AlgorithmicPlatformInterfaceDebug(AlgorithmicPlatformInterface):
    """
    this class is only meant as a debug/etc, not for productive use!
    Interface to the algorithmic platform of VIRIATO. A wrapper around the REST-API.
    """

    def some_action(self) -> None:
        print('nothing to see here, i am a placeholder')

    def do_request(self, request_str, request_type, request_body=None, params_dict=None) -> requests.Response:
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
