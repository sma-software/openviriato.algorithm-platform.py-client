"""
This is the module intended to act as an interface to the algorithmic platform of VIRIATO
Wraps around the REST-API to enhance the usability. It consists of the interface with the requests as methods.
"""

__all__ = ['AlgorithmicPlatformInterface']
__version__ = '0.0.1'
__author__ = 'Florian Fuchs'

import requests
import json
import AlgorithmClasses
import AlgorithmStatic


def initialise_algorithm_node_from_dict(node_as_dict: dict) -> AlgorithmClasses.AlgorithmNode:
    return AlgorithmClasses.AlgorithmNode(node_id=node_as_dict['ID'],
                                          code_string=node_as_dict['Code'],
                                          node_tracks=node_as_dict['NodeTracks'],
                                          debug_string=node_as_dict['DebugString'])


def initialise_algorithm_node_list(list_of_nodes_as_dict: list) -> list:
    return [initialise_algorithm_node_from_dict(node_as_dict) for node_as_dict in list_of_nodes_as_dict]


def initialise_algorithm_section_track_from_dict(section_track_as_dict: dict) -> AlgorithmClasses.AlgorithmSectionTrack:
    return AlgorithmClasses.AlgorithmSectionTrack(section_id=section_track_as_dict['ID'],
                                                  code_string=section_track_as_dict['Code'],
                                                  section_code=section_track_as_dict['SectionCode'],
                                                  debug_string=section_track_as_dict['DebugString'],
                                                  section_weight=section_track_as_dict['Weight'])


def initialise_algorithm_section_track_list(list_of_sections_dict: list) -> list:
    return [initialise_algorithm_section_track_from_dict(section_as_dict) for section_as_dict in list_of_sections_dict]


class JSONObject:
    def __init__(self, json_as_dict):
        Warning('returning response as an Object, no check for consistency')
        vars(self).update(json_as_dict)


class AlgorithmicPlatformInterface:
    """
    Interface to the algorithmic platform of VIRIATO. A wrapper around the REST-API.
    Supports and is intended to be used in with statements
    """
    __base_url: str
    __currentSession: requests.Session()

    def __init__(self, base_url: str):
        AlgorithmStatic.assert_parameter_is_str(base_url, 'base_url', '__init__')
        self.__base_url = base_url
        self.__currentSession = requests.Session()

    def __enter__(self):
        return self  # to be used in with statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__currentSession.close()

    def __merge_base_url_with_request(self, request: str) -> str:
        return '{0}/{1}'.format(self.__base_url, request)

    def __do_get_request(self, request_call: str, request_param: dict = None) -> requests.Response:
        if request_param is None:
            request_param = {}
        complete_url = self.__merge_base_url_with_request(request_call)
        api_response = self.__currentSession.get(complete_url, params=request_param)
        AlgorithmStatic.check_if_request_successful(api_response)
        return api_response

    def __do_post_request(self, request_call: str, request_body: dict = None) -> requests.Response:
        if request_body is None:
            request_body = {}
        complete_url = self.__merge_base_url_with_request(request_call)
        api_response = self.__currentSession.post(complete_url, json=request_body)
        AlgorithmStatic.check_if_request_successful(api_response)
        return api_response

    def __do_put_request(self, request_call: str, request_body: dict = None) -> requests.Response:
        if request_body is None:
            request_body = {}
        complete_url = self.__merge_base_url_with_request(request_call)
        api_response = self.__currentSession.put(complete_url, json=request_body)
        AlgorithmStatic.check_if_request_successful(api_response)
        return api_response

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
        request_body = {'messageLevel1': message_level_1, 'messageLevel2': message_level_2}
        self.__do_post_request('notifications', request_body)

    def show_status_message(self, short_message: str, long_message=None) -> None:
        """
        Notify the user of VIRIATO with information on the status bar
        :param short_message: str
        :param long_message: str, None if not required
        """
        AlgorithmStatic.assert_parameter_is_str(short_message, 'short_message', 'show_status_message')
        if not (long_message is None):
            AlgorithmStatic.assert_parameter_is_str(short_message, 'long_message', 'show_status_message')
        request_body = {'shortMessage': short_message, 'longMessage': long_message}
        self.__do_post_request('status-message', request_body)

    def get_neighbor_nodes(self, node_id: int) -> list:
        """
        Returns a list of all neighbor nodes of the given node x with nodeID == node_id, that is, all nodes y such
        that there exists at least one section track directly from x to y.
        :param node_id: int
        :return: list, containing all tracks
        """
        AlgorithmStatic.assert_parameter_is_int(node_id, 'node_id', 'get_neighbor_nodes')
        url_tail = 'neighbor-nodes/{0}'.format(node_id)
        api_response = self.__do_get_request(url_tail)
        return initialise_algorithm_node_list(api_response.json())

    def get_node(self, node_id: int) -> AlgorithmClasses.AlgorithmNode:
        """
        Returns an IAlgorithm​Node dict for the given node_id
        :param node_id: int
        :return: dict,
        """
        AlgorithmStatic.assert_parameter_is_int(node_id, 'node_id', 'get_node')
        url_tail = 'nodes/{0}'.format(node_id)
        api_response = self.__do_get_request(url_tail)
        return initialise_algorithm_node_from_dict(api_response.json())

    def get_directed_section_tracks(self, first_node_id: int, second_node_id: int) -> list:
        """
        get all tracks in direction of the section between the two nodes. Direction given by order of the nodes
        :param first_node_id: int
        :param second_node_id: int
        :return: tuple, containing all tracks, empty if no tracks exist
        """
        AlgorithmStatic.assert_parameter_is_int(first_node_id, 'first_node_id', 'get_directed_section_tracks')
        AlgorithmStatic.assert_parameter_is_int(second_node_id, 'second_node_id', 'get_directed_section_tracks')
        url_tail = 'section-tracks-between/{0}/{1}'.format(first_node_id, second_node_id)
        api_response = self.__do_get_request(url_tail)
        return initialise_algorithm_section_track_list(api_response.json())

    def get_parallel_section_tracks(self, section_track_id: int) -> list:
        """
        Returns a list of all section tracks starting and ending at the same nodes as the section track with id
        section_track_id independent of the traffic-ability.
        The track with id section_track_id is included in the result.
        :param section_track_id: int
        :return: tuple
        """
        AlgorithmStatic.assert_parameter_is_int(section_track_id, 'section_track_id', 'get_parallel_section_tracks')
        url_tail = 'section-tracks-parallel-to/{0}'.format(section_track_id)
        api_response = self.__do_get_request(url_tail)
        return initialise_algorithm_section_track_list(api_response.json())

    def get_train_classification(self, train_id: int) -> dict:
        AlgorithmStatic.assert_parameter_is_int(train_id, 'train_id', 'get_train_classification')
        api_response = self.__do_get_request('train-classification/{0}'.format(train_id))
        raise api_response.json()

    def get_train_classifications(self) -> dict:
        api_response = self.__do_get_request('train-classifications')
        return api_response.json()

    def cancel_train_from(self, train_path_node_id: int) -> JSONObject:  # AlgorithmClasses.AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmStatic.assert_parameter_is_int(train_path_node_id, 'train_path_node_od', 'cancel_train_from')
        post_request_body = {'trainPathNodeID': train_path_node_id}
        api_response = self.__do_post_request('cancel-train-from', request_body=post_request_body)
        return json.loads(api_response.content, object_hook=JSONObject)

    def cancel_train_to(self, train_path_node_id: int) -> JSONObject:  # AlgorithmClasses.AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmStatic.assert_parameter_is_int(train_path_node_id, 'train_path_node_od', 'cancel_train_to')
        post_request_body = {'trainPathNodeID': train_path_node_id}
        api_response = self.__do_post_request('cancel-train-to', request_body=post_request_body)
        return json.loads(api_response.content, object_hook=JSONObject)

    def clone_train(self, train_id: int) -> JSONObject:  # AlgorithmClasses.AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmStatic.assert_parameter_is_int(train_id, 'train_id', 'clone_train')
        post_request_body = {'TrainID': train_id}
        api_response = self.__do_post_request('clone-train', request_body=post_request_body)
        return json.loads(api_response.content, object_hook=JSONObject)

    def set_station_track(self, train_path_node_id: int,
                          section_track_id: int) -> JSONObject:  # AlgorithmClasses.AlgorithmTrain:
        AlgorithmStatic.assert_parameter_is_int(train_path_node_id, 'train_path_node_id', 'set_station_track')
        AlgorithmStatic.assert_parameter_is_int(section_track_id, 'section_track_id', 'set_station_track')
        post_request_body = {'trainPathNodeID': train_path_node_id, 'sectionTrackID': section_track_id}
        api_response = self.__do_post_request('set-section-track', request_body=post_request_body)
        return json.loads(api_response.content, object_hook=JSONObject)

    def update_train_times(self, train_id: int,
                           update_train_times_node: list) -> JSONObject:  # AlgorithmClasses.AlgorithmTrain:
        AlgorithmStatic.assert_parameter_is_int(train_id)
        assert isinstance(update_train_times_node, list), 'update_train_times_node must be a list of nodes'
        for node in update_train_times_node:
            assert isinstance(node, AlgorithmClasses.UpdateTrainTimesNode), \
                'all objects in update_train_times_node must be of type UpdateTrainTimesNode'
        url_tail = 'trains/{0}/train-path-nodes'.format(train_id)
        latest_api_content = None
        for node in update_train_times_node:
            put_body = {'TrainPathNodeId': node.TrainPathNodeID, 'ArrivalTime': node.ArrivalTime,
                        'DepartureTime': node.DepartureTime, 'MinimumRunTime': node.MinimumRunTime,
                        'MinimumStopTime': node.MinimumStopTime, 'StopStatus': node.StopStatus}
            api_response = self.__do_put_request(url_tail, request_body=put_body)
            latest_api_content = api_response.content
        return json.loads(latest_api_content, object_hook=JSONObject)


class AlgorithmicPlatformInterfaceIncomplete(AlgorithmicPlatformInterface):

    def reroute_train(self, route: NotImplementedError) -> JSONObject:  # AlgorithmClasses.AlgorithmTrain:
        raise NotImplementedError
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        assert ()

    def get_vehicle_type(self, vehicle_type_id: int) -> NotImplementedError:
        raise NotImplementedError

    # train methods
    def get_trains(self, time_window: AlgorithmClasses.AlgorithmTimeWindow) -> NotImplementedError:
        raise NotImplementedError

    def get_trains_driving_any_node(self, time_window: AlgorithmClasses.AlgorithmTimeWindow, node_list: list) -> \
            NotImplementedError:
        raise NotImplementedError

    def get_trains_cut_to_time_range(self, time_window: AlgorithmClasses.AlgorithmTimeWindow) -> NotImplementedError:
        raise NotImplementedError

    def get_trains_cut_to_time_range_driving_any_node(self, time_window: AlgorithmClasses.AlgorithmTimeWindow,
                                                      node_list: list) -> NotImplementedError:
        raise NotImplementedError


class JSONObject:
    def __init__(self, json_as_dict):
        Warning('returning response as an Object, no check for consistency')
        vars(self).update(json_as_dict)