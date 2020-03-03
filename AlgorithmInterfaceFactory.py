"""
This is the module intended to act as an interface to the algorithmic platform of VIRIATO
Wraps around the REST-API to enhance the usability. It consists of the interface with the requests as methods.
"""

__all__ = ['AlgorithmicPlatformInterface']
__version__ = '0.0.1'
__author__ = 'Florian Fuchs'

import AIDM_module.AIDM_factories
import AlgorithmInterfaceCommunicationLayer
import AlgorithmTypeCheck
from AIDM_module import AIDM_classes
from AIDM_module.AIDM_factories import dict_to_algorithm_node_factory, list_of_dicts_to_algorithm_node_list_factory, \
    dict_to_algorithm_section_track_factory, algorithm_section_track_list_factory

class AlgorithmicPlatformInterface: # AlgorithmInterface
    __communication_layer: AlgorithmInterfaceCommunicationLayer.CommunicationLayer

    def __init__(self, base_url: str):
        self.__communication_layer = AlgorithmInterfaceCommunicationLayer.CommunicationLayer(base_url)

    def __enter__(self):
        return self  # to be used in with statement as disposable

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.__communication_layer.currentSession.close()  # to be used in with statement as disposable

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
        return list_of_dicts_to_algorithm_node_list_factory(api_response.json())

    def get_node(self, node_id: int) -> AIDM_classes.AlgorithmNode:
        AlgorithmTypeCheck.assert_parameter_is_int(node_id, 'node_id', 'get_node')
        api_response = self.__communication_layer.do_get_request('nodes/{0}'.format(node_id))
        return dict_to_algorithm_node_factory(api_response.json())

    def get_section_track(self, section_track_id: int) -> AIDM_classes.AlgorithmSectionTrack:
        AlgorithmTypeCheck.assert_parameter_is_int(section_track_id, 'section_track_id', 'get_section_track')
        url_tail = 'section-tracks/{0}'.format(section_track_id)
        api_response = self.__communication_layer.do_get_request(url_tail)
        return dict_to_algorithm_section_track_factory(api_response.json())

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

    def cancel_train(self, train_id: int) -> AIDM_classes.AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmTypeCheck.assert_parameter_is_int(train_id, 'train_id', 'cancel_train')
        api_response = self.__communication_layer.do_post_request('cancel-train', request_body={'trainID': train_id})
        return api_response.json()['trainID']

    def cancel_train_from(self, train_path_node_id: int) -> AIDM_classes.AlgorithmTrain:
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_id', 'cancel_train_from')
        post_request_body = {'trainPathNodeID': train_path_node_id}
        api_response = self.__communication_layer.do_post_request('cancel-train-from', request_body=post_request_body)
        return AIDM_module.AIDM_factories.dict_to_algorithm_train_factory(api_response.json())

    def cancel_train_to(self, train_path_node_id: int) -> AIDM_classes.AlgorithmTrain:
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_id', 'cancel_train_to')
        post_request_body = {'trainPathNodeID': train_path_node_id}
        api_response = self.__communication_layer.do_post_request('cancel-train-to', request_body=post_request_body)
        return AIDM_module.AIDM_factories.dict_to_algorithm_train_factory(api_response.json())

    def clone_train(self, train_id: int) -> AIDM_classes.AlgorithmTrain:
        AlgorithmTypeCheck.assert_parameter_is_int(train_id, 'train_id', 'clone_train')
        post_request_body = {'TrainID': train_id}
        api_response = self.__communication_layer.do_post_request('clone-train', request_body=post_request_body)
        return AIDM_module.AIDM_factories.dict_to_algorithm_train_factory(api_response.json())

    def set_section_track(self, train_path_node_id: int, section_track_id: int) -> AIDM_classes.AlgorithmTrain:
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_id', 'set_section_track')
        AlgorithmTypeCheck.assert_parameter_is_int(section_track_id, 'section_track_id', 'set_section_track')
        post_request_body = {'TrainPathNodeID': train_path_node_id, 'SectionTrackID': section_track_id}
        api_response = self.__communication_layer.do_post_request('set-section-track', request_body=post_request_body)
        return AIDM_module.AIDM_factories.dict_to_algorithm_train_factory(api_response.json())

    def update_train_times(self, train_id: int, update_train_times_node: list) -> AIDM_classes.AlgorithmTrain:
        AlgorithmTypeCheck.assert_parameter_is_int(train_id, 'train_id', 'update_train_times')
        url_tail = 'trains/{0}/train-path-nodes'.format(train_id)
        put_body_list = [{'TrainPathNodeId': node.TrainPathNodeID, 'ArrivalTime': node.ArrivalTime,
                          'DepartureTime': node.DepartureTime, 'MinimumRunTime': node.MinimumRunTime,
                          'MinimumStopTime': node.MinimumStopTime, 'StopStatus': node.StopStatus}
                         for node in update_train_times_node]
        api_response = self.__communication_layer.do_put_request(url_tail, request_body=put_body_list)
        return AIDM_module.AIDM_factories.dict_to_algorithm_train_factory(api_response.json())



def create(base_url: str):
    return AlgorithmicPlatformInterface(base_url=base_url)

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
