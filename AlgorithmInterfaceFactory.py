"""
This is the module intended to act as an interface to the algorithmic platform of VIRIATO
Wraps around the REST-API to enhance the usability. It consists of the interface with the requests as methods.
"""

__all__ = ['AlgorithmicPlatformInterface']
__version__ = '0.0.1'
__author__ = 'Florian Fuchs'

import datetime
import warnings

import AlgorithmInterfaceCommunicationLayer
import converter_module.converter_helpers
import converter_module.from_AIDM_converter
import converter_module.to_AIDM_converter
from AIDM_module import AIDM_classes


class AlgorithmicPlatformInterface:  # AlgorithmInterface
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
        request_body = {'messageLevel1': message_level_1, 'messageLevel2': message_level_2}
        self.__communication_layer.do_post_request('notifications', request_body)

    def show_status_message(self, short_message: str, long_message=None) -> None:
        request_body = {'shortMessage': short_message, 'longMessage': long_message}
        self.__communication_layer.do_post_request('status-message', request_body)

    def get_node(self, node_id: int) -> AIDM_classes.AlgorithmNode:
        response_dict = self.__communication_layer.do_get_request('nodes/{0}'.format(node_id))
        return converter_module.to_AIDM_converter.convert_dict_to_AlgorithmNode(response_dict)

    def get_neighbor_nodes(self, node_id: int) -> list:
        response_list = self.__communication_layer.do_get_request('neighbor-nodes/{0}'.format(node_id))
        return converter_module.to_AIDM_converter.convert_list_of_dict_to_AlgorithmNode(response_list)

    def get_section_track(self, section_track_id: int) -> AIDM_classes.AlgorithmSectionTrack:
        response_dict = self.__communication_layer.do_get_request('section-tracks/{0}'.format(section_track_id))
        return converter_module.to_AIDM_converter.convert_dict_to_AIDM(
            AIDM_classes.AlgorithmSectionTrack, response_dict)

    def get_directed_section_tracks(self, first_node_id: int, second_node_id: int) -> list:
        url_tail = 'section-tracks-between/{0}/{1}'.format(first_node_id, second_node_id)
        response_list = self.__communication_layer.do_get_request(url_tail)
        return converter_module.to_AIDM_converter.from_list_of_dict_to_list_of_AIDM(
            AIDM_classes.AlgorithmSectionTrack, response_list)

    def get_parallel_section_tracks(self, section_track_id: int) -> list:
        url_tail = 'section-tracks-parallel-to/{0}'.format(section_track_id)
        response_list = self.__communication_layer.do_get_request(url_tail)
        return converter_module.to_AIDM_converter.from_list_of_dict_to_list_of_AIDM(
            AIDM_classes.AlgorithmSectionTrack, response_list)

    def get_train_classification(self, train_id: int) -> dict:
        return self.__communication_layer.do_get_request('train-classification/{0}'.format(train_id))

    def get_train_classifications(self) -> dict:
        return self.__communication_layer.do_get_request('train-classifications')

    def cancel_train(self, train_id: int) -> int:
        response_dict = self.__communication_layer.do_post_request('cancel-train', request_body={'trainID': train_id})
        return response_dict['trainID']

    def cancel_train_from(self, train_path_node_id: int) -> AIDM_classes.AlgorithmTrain:
        post_request_body = {'trainPathNodeID': train_path_node_id}
        response_dict = self.__communication_layer.do_post_request('cancel-train-from', request_body=post_request_body)
        return converter_module.to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def cancel_train_to(self, train_path_node_id: int) -> AIDM_classes.AlgorithmTrain:
        post_request_body = {'trainPathNodeID': train_path_node_id}
        response_dict = self.__communication_layer.do_post_request('cancel-train-to', request_body=post_request_body)
        return converter_module.to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def clone_train(self, train_id: int) -> AIDM_classes.AlgorithmTrain:
        post_request_body = {'TrainID': train_id}
        response_dict = self.__communication_layer.do_post_request('clone-train', request_body=post_request_body)
        return converter_module.to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def set_section_track(self, train_path_node_id: int, section_track_id: int) -> AIDM_classes.AlgorithmTrain:
        post_request_body = {'TrainPathNodeID': train_path_node_id, 'SectionTrackID': section_track_id}
        response_dict = self.__communication_layer.do_post_request('set-section-track', request_body=post_request_body)
        return converter_module.to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def update_train_times(self, train_id: int, update_train_times_nodes: list) -> AIDM_classes.AlgorithmTrain:
        url_tail = 'trains/{0}/train-path-nodes'.format(train_id)
        put_body_list = converter_module.from_AIDM_converter.convert_to_list_of_dict(update_train_times_nodes)
        response_dict = self.__communication_layer.do_put_request(url_tail, request_body=put_body_list)
        return converter_module.to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def get_headway_time_for_train_path_nodes(self, preceding_train_path_node_id: int,
                                              succeeding_train_path_node_id: int) -> datetime.timedelta:
        url_tail = 'headway-times/between-train-path-nodes/{0}/{1}'.format(preceding_train_path_node_id,
                                                                           succeeding_train_path_node_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return converter_module.converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_headway_time_for_train_path_nodes_on_section_track(self, preceding_train_path_node_id: int,
                                                               succeeding_train_path_node_id: int,
                                                               section_track_id: int, from_node_id: int,
                                                               to_node_id: int) -> datetime.timedelta:
        url_tail = 'headway-times/between-train-path-nodes/{0}/{1}/for-section-track/{2}/in-direction/{3}/{4}'.format(
            preceding_train_path_node_id, succeeding_train_path_node_id, section_track_id, from_node_id, to_node_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return converter_module.converter_helpers.parse_to_timedelta(response_dict["headwayTime"])

    def get_separation_time_in_junction(self, preceding_train_path_node_id: int, succeeding_train_path_node_id: int
                                        ) -> datetime.timedelta:
        url_tail = 'junction-separation-time/between-train-path-nodes/{0}/{1}'.format(preceding_train_path_node_id,
                                                                                      succeeding_train_path_node_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        warnings.warn("Not Tested Yet")
        return converter_module.converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_station_track_reoccupation_separation_time(self, preceding_train_path_node_id: int,
                                                       succeeding_train_path_node_id: int, node_track_id: int
                                                       ) -> datetime.timedelta:
        url_tail = 'station-track-reoccupation-separation-time/{0}/{1}/{2}'.format(preceding_train_path_node_id,
                                                                                   succeeding_train_path_node_id,
                                                                                   node_track_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        warnings.warn("Not Tested Yet")
        return converter_module.converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_separation_time_in_any_junction(self, tbd: NotImplementedError) -> datetime.timedelta:
        raise NotImplementedError
        return converter_module.converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_separation_time_in_station(self, tbd: NotImplementedError) -> datetime.timedelta:
        raise NotImplementedError
        return converter_module.converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_separation_time_in_station_for_entry_or_exit(self, tbd: NotImplementedError) -> datetime.timedelta:
        raise NotImplementedError
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return converter_module.converter_helpers.parse_to_timedelta(response_dict["separationTime"])

def create(base_url: str):
    return AlgorithmicPlatformInterface(base_url=base_url)
