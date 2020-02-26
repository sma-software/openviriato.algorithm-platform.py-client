"""
This is the module intended to act as an interface to the algorithmic platform of VIRIATO
Wraps around the REST-API to enhance the usability. It consists of the interface with the requests as methods.
"""

__all__ = ['AlgorithmicPlatformInterface']
__version__ = '0.0.1'
__author__ = 'Florian Fuchs'

import AIDMClasses
import AlgorithmTypeCheck
import AlgorithmInterfaceCommunicationLayer


def algorithm_node_track_from_dict_factory(node_track_as_dict: dict) -> AIDMClasses.AlgorithmNodeTrack:
    return AIDMClasses.AlgorithmNodeTrack(node_track_id=node_track_as_dict['ID'],
                                          code_string=node_track_as_dict['Code'],
                                          debug_string=node_track_as_dict['DebugString'])


def algorithm_node_from_dict_factory(node_as_dict: dict) -> AIDMClasses.AlgorithmNode:
    node_track_list = None
    if not node_as_dict['NodeTracks'] is None:
        node_track_list = []
        for node_track in node_as_dict['NodeTracks']:
            node_track_list.append(algorithm_node_track_from_dict_factory(node_track))
    return AIDMClasses.AlgorithmNode(node_id=node_as_dict['ID'],
                                     code_string=node_as_dict['Code'],
                                     node_tracks=node_track_list,
                                     debug_string=node_as_dict['DebugString'])


def algorithm_node_list_factory(list_of_nodes_as_dict: list) -> list:
    return [algorithm_node_from_dict_factory(node_as_dict) for node_as_dict in list_of_nodes_as_dict]


def algorithm_section_track_from_dict_factory(section_track_as_dict: dict) -> AIDMClasses.AlgorithmSectionTrack:
    return AIDMClasses.AlgorithmSectionTrack(section_id=section_track_as_dict['ID'],
                                             code_string=section_track_as_dict['Code'],
                                             section_code=section_track_as_dict['SectionCode'],
                                             debug_string=section_track_as_dict['DebugString'],
                                             section_weight=section_track_as_dict['Weight'])


def algorithm_section_track_list_factory(list_of_sections_dict: list) -> list:
    return [algorithm_section_track_from_dict_factory(section_as_dict) for section_as_dict in list_of_sections_dict]


def check_attributes_by_list(obj, attribute_names: list):
    for attribute_name in attribute_names:
        assert (hasattr(obj, attribute_name)), 'attribute {0} is missing'.format(attribute_name)


class AlgorithmicPlatformInterface:
    __communication_layer: AlgorithmInterfaceCommunicationLayer.CommunicationLayer

    def __init__(self, base_url: str):
        self.__communication_layer = AlgorithmInterfaceCommunicationLayer.CommunicationLayer(base_url)

    def __enter__(self):
        return self  # to be used in with statement as disposable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__communication_layer.currentSession.close() # to be used in with statement as disposable

    @property
    def base_url(self) -> str:
        return self.__communication_layer.base_url

    def notify_user(self, message_level_1: str, message_level_2: str) -> None:
        AlgorithmTypeCheck.assert_parameter_is_str(message_level_1, 'message_level_1', 'notify_user')
        AlgorithmTypeCheck.assert_parameter_is_str(message_level_2, 'message_level_2', 'notify_user')
        request_body = {'messageLevel1': message_level_1, 'messageLevel2': message_level_2}
        self.__communication_layer.do_post_request('notifications', request_body)

    def show_status_message(self, short_message: str, long_message=None) -> None:
        AlgorithmTypeCheck.assert_parameter_is_str(short_message, 'short_message', 'show_status_message')
        if not (long_message is None):
            AlgorithmTypeCheck.assert_parameter_is_str(long_message, 'long_message', 'show_status_message')
        request_body = {'shortMessage': short_message, 'longMessage': long_message}
        self.__communication_layer.do_post_request('status-message', request_body)

    def get_neighbor_nodes(self, node_id: int) -> list:
        AlgorithmTypeCheck.assert_parameter_is_int(node_id, 'node_id', 'get_neighbor_nodes')
        api_response = self.__communication_layer.do_get_request('neighbor-nodes/{0}'.format(node_id))
        return algorithm_node_list_factory(api_response.json())

    def get_node(self, node_id: int) -> AIDMClasses.AlgorithmNode:
        AlgorithmTypeCheck.assert_parameter_is_int(node_id, 'node_id', 'get_node')
        api_response = self.__communication_layer.do_get_request('nodes/{0}'.format(node_id))
        return algorithm_node_from_dict_factory(api_response.json())

    def get_section_track(self, section_track_id: int) -> AIDMClasses.AlgorithmSectionTrack:
        AlgorithmTypeCheck.assert_parameter_is_int(section_track_id, 'section_track_id', 'get_section_track')
        url_tail = 'section-tracks/{0}'.format(section_track_id)
        api_response = self.__communication_layer.do_get_request(url_tail)
        return algorithm_section_track_from_dict_factory(api_response.json())

    def get_directed_section_tracks(self, first_node_id: int, second_node_id: int) -> list:
        AlgorithmTypeCheck.assert_parameter_is_int(first_node_id, 'first_node_id', 'get_directed_section_tracks')
        AlgorithmTypeCheck.assert_parameter_is_int(second_node_id, 'second_node_id', 'get_directed_section_tracks')
        url_tail = 'section-tracks-between/{0}/{1}'.format(first_node_id, second_node_id)
        api_response = self.__communication_layer.do_get_request(url_tail)
        return algorithm_section_track_list_factory(api_response.json())

    def get_parallel_section_tracks(self, section_track_id: int) -> list:
        AlgorithmTypeCheck.assert_parameter_is_int(section_track_id, 'section_track_id', 'get_parallel_section_tracks')
        api_response = self.__communication_layer.do_get_request(
            'section-tracks-parallel-to/{0}'.format(section_track_id))
        return algorithm_section_track_list_factory(api_response.json())

    def get_train_classification(self, train_id: int) -> dict:
        AlgorithmTypeCheck.assert_parameter_is_int(train_id, 'train_id', 'get_train_classification')
        api_response = self.__communication_layer.do_get_request('train-classification/{0}'.format(train_id))
        return api_response.json()

    def get_train_classifications(self) -> dict:
        api_response = self.__communication_layer.do_get_request('train-classifications')
        return api_response.json()

    def cancel_train(self, train_id: int) -> AIDMClasses.AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmTypeCheck.assert_parameter_is_int(train_id, 'train_id', 'cancel_train')
        api_response = self.__communication_layer.do_post_request('cancel-train', request_body={'trainID': train_id})
        return api_response.json()['trainID']

    def cancel_train_from(self, train_path_node_id: int) -> AIDMClasses.AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_id', 'cancel_train_from')
        post_request_body = {'trainPathNodeID': train_path_node_id}
        api_response = self.__communication_layer.do_post_request('cancel-train-from', request_body=post_request_body)
        return AIDMClasses.dict_to_algorithm_train_factory(api_response.json())

    def cancel_train_to(self, train_path_node_id: int) -> AIDMClasses.AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_id', 'cancel_train_to')
        post_request_body = {'trainPathNodeID': train_path_node_id}
        api_response = self.__communication_layer.do_post_request('cancel-train-to', request_body=post_request_body)
        return AIDMClasses.dict_to_algorithm_train_factory(api_response.json())

    def clone_train(self, train_id: int) -> AIDMClasses.AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmTypeCheck.assert_parameter_is_int(train_id, 'train_id', 'clone_train')
        post_request_body = {'TrainID': train_id}
        api_response = self.__communication_layer.do_post_request('clone-train', request_body=post_request_body)
        return AIDMClasses.dict_to_algorithm_train_factory(api_response.json())

    def set_station_track(self, train_path_node_id: int, section_track_id: int) -> AIDMClasses.AlgorithmTrain:
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_id', 'set_station_track')
        AlgorithmTypeCheck.assert_parameter_is_int(section_track_id, 'section_track_id', 'set_station_track')
        post_request_body = {'trainPathNodeID': train_path_node_id, 'sectionTrackID': section_track_id}
        api_response = self.__communication_layer.do_post_request('set-section-track', request_body=post_request_body)
        return AIDMClasses.dict_to_algorithm_train_factory(api_response.json())

    def update_train_times(self, train_id: int, update_train_times_node: list) -> AIDMClasses.AlgorithmTrain:
        AlgorithmTypeCheck.assert_parameter_is_int(train_id, 'train_id', 'update_train_times')
        url_tail = 'trains/{0}/train-path-nodes'.format(train_id)
        put_body_list = [{'TrainPathNodeId': node.TrainPathNodeID, 'ArrivalTime': node.ArrivalTime,
                          'DepartureTime': node.DepartureTime, 'MinimumRunTime': node.MinimumRunTime,
                          'MinimumStopTime': node.MinimumStopTime, 'StopStatus': node.StopStatus}
                         for node in update_train_times_node]
        api_response = self.__communication_layer.do_put_request(url_tail, request_body=put_body_list)
        return AIDMClasses.dict_to_algorithm_train_factory(api_response.json())


"""
class AlgorithmicPlatformInterfaceIncomplete(AlgorithmicPlatformInterface):
    class GenericObjectFromJson:
        def __init__(self, json_as_dict):
            vars(self).update(json_as_dict)

    def reroute_train(self,
                      route: NotImplementedError) -> GenericObjectFromJson:  # AlgorithmClasses.AlgorithmTrain:
        raise NotImplementedError
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        assert ()

    def get_vehicle_type(self, vehicle_type_id: int) -> NotImplementedError:
        raise NotImplementedError

    # train methods
    def get_trains(self, time_window: AIDMClasses.AlgorithmTimeWindow) -> NotImplementedError:
        raise NotImplementedError

    def get_trains_driving_any_node(self, time_window: AIDMClasses.AlgorithmTimeWindow, node_list: list) -> \
            NotImplementedError:
        raise NotImplementedError

    def get_trains_cut_to_time_range(self, time_window: AIDMClasses.AlgorithmTimeWindow) -> NotImplementedError:
        raise NotImplementedError

    def get_trains_cut_to_time_range_driving_any_node(self, time_window: AIDMClasses.AlgorithmTimeWindow,
                                                      node_list: list) -> NotImplementedError:
        raise NotImplementedError
"""
