__version__ = '0.0.1'
__author__ = 'Florian Fuchs'

import datetime
import warnings

from AIDMClasses import AIDM_classes, AIDM_enum_classes
from AlgorithmInterface.AlgorithmInterfaceHelpers import extract_parameters_from_routing_point, \
    add_cut_train_to_get_request_params, add_node_filter_to_get_request_params
from CommunicationLayer import AlgorithmInterfaceCommunicationLayer
from ConversionLayer import converter_helpers, to_AIDM_converter, from_AIDM_converter


class AlgorithmicPlatformInterface:
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
        return to_AIDM_converter.convert_dict_to_AlgorithmNode(response_dict)

    def get_neighbor_nodes(self, node_id: int) -> list:
        response_list = self.__communication_layer.do_get_request('neighbor-nodes/{0}'.format(node_id))
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(
            to_AIDM_converter.convert_dict_to_AlgorithmNode, response_list)

    def get_section_track(self, section_track_id: int) -> AIDM_classes.AlgorithmSectionTrack:
        response_dict = self.__communication_layer.do_get_request('section-tracks/{0}'.format(section_track_id))
        return to_AIDM_converter.convert_dict_to_AIDM(AIDM_classes.AlgorithmSectionTrack, response_dict)

    def get_directed_section_tracks(self, first_node_id: int, second_node_id: int) -> list:
        url_tail = 'section-tracks-between/{0}/{1}'.format(first_node_id, second_node_id)
        response_list = self.__communication_layer.do_get_request(url_tail)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(AIDM_classes.AlgorithmSectionTrack, response_list)

    def get_parallel_section_tracks(self, section_track_id: int) -> list:
        url_tail = 'section-tracks-parallel-to/{0}'.format(section_track_id)
        response_list = self.__communication_layer.do_get_request(url_tail)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(AIDM_classes.AlgorithmSectionTrack, response_list)

    def get_train_classification(self, train_id: int) -> dict:
        return self.__communication_layer.do_get_request('train-classification/{0}'.format(train_id))

    def get_train_classifications(self) -> dict:
        return self.__communication_layer.do_get_request('train-classifications')

    def get_trains(self, timeWindow: AIDM_classes.TimeWindow) -> list:
        warnings.warn("not tested")
        url_tail = "trains"
        get_request_params = from_AIDM_converter.convert_to_json_conform_dict(timeWindow)
        response_list = self.__communication_layer.do_get_request(url_tail, request_param=get_request_params)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(
            to_AIDM_converter.convert_dict_to_AlgorithmTrain, response_list)

    def get_trains_driving_any_node(self, timeWindow: AIDM_classes.TimeWindow, nodeIDs: list) -> list:
        warnings.warn("not tested")
        url_tail = "trains"
        get_request_params = from_AIDM_converter.convert_to_json_conform_dict(timeWindow)
        get_request_params = add_node_filter_to_get_request_params(get_request_params, nodeIDs)
        response_list = self.__communication_layer.do_get_request(url_tail, request_param=get_request_params)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(
            to_AIDM_converter.convert_dict_to_AlgorithmTrain, response_list)

    def get_trains_cut_to_time_range(self, timeWindow: AIDM_classes.TimeWindow) -> list:
        warnings.warn("not tested")
        url_tail = "trains"
        get_request_params = from_AIDM_converter.convert_to_json_conform_dict(timeWindow)
        get_request_params = add_cut_train_to_get_request_params(get_request_params)
        response_list = self.__communication_layer.do_get_request(url_tail, request_param=get_request_params)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(
            to_AIDM_converter.convert_dict_to_AlgorithmTrain, response_list)

    def get_trains_cut_to_time_range_driving_any_node(self, timeWindow: AIDM_classes.TimeWindow, nodeIDs: list) -> list:
        warnings.warn("not tested")
        url_tail = "trains"
        get_request_params = from_AIDM_converter.convert_to_json_conform_dict(timeWindow)
        get_request_params = add_node_filter_to_get_request_params(get_request_params, nodeIDs)
        get_request_params = add_cut_train_to_get_request_params(get_request_params)
        response_list = self.__communication_layer.do_get_request(url_tail, request_param=get_request_params)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(
            to_AIDM_converter.convert_dict_to_AlgorithmTrain, response_list)

    def cancel_train(self, train_id: int) -> int:
        return self.__communication_layer.do_post_request('cancel-train', request_body={'trainID': train_id})

    def cancel_train_from(self, train_path_node_id: int) -> AIDM_classes.AlgorithmTrain:
        post_request_body = {'trainPathNodeID': train_path_node_id}
        response_dict = self.__communication_layer.do_post_request('cancel-train-from', request_body=post_request_body)
        return to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def cancel_train_to(self, train_path_node_id: int) -> AIDM_classes.AlgorithmTrain:
        post_request_body = {'trainPathNodeID': train_path_node_id}
        response_dict = self.__communication_layer.do_post_request('cancel-train-to', request_body=post_request_body)
        return to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def clone_train(self, train_id: int) -> AIDM_classes.AlgorithmTrain:
        post_request_body = {'TrainID': train_id}
        response_dict = self.__communication_layer.do_post_request('clone-train', request_body=post_request_body)
        return to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def reroute_train(self, route: AIDM_classes.UpdateTrainRoute):
        url_tail = "reroute-train"
        post_request_body = from_AIDM_converter.convert_to_json_conform_dict(route)
        response_dict = self.__communication_layer.do_post_request(url_tail, request_body=post_request_body)
        return to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def set_section_track(self, train_path_node_id: int, section_track_id: int) -> AIDM_classes.AlgorithmTrain:
        post_request_body = {'TrainPathNodeID': train_path_node_id, 'SectionTrackID': section_track_id}
        response_dict = self.__communication_layer.do_post_request('set-section-track', request_body=post_request_body)
        return to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def update_train_times(self, train_id: int, update_train_times_nodes: list) -> AIDM_classes.AlgorithmTrain:
        url_tail = 'trains/{0}/train-path-nodes'.format(train_id)
        put_body_list = from_AIDM_converter.convert_to_list_of_dict(update_train_times_nodes)
        response_dict = self.__communication_layer.do_put_request(url_tail, request_body=put_body_list)
        return to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def update_trajectory(self, train_id: int, update_train_stop_times_nodes: list) -> AIDM_classes.AlgorithmTrain:
        url_tail = "trains/{0}/train-path-nodes:update-trajectory-stop-times".format(train_id)
        put_body_list = from_AIDM_converter.convert_to_list_of_dict(update_train_stop_times_nodes)
        response_dict = self.__communication_layer.do_put_request(url_tail, request_body=put_body_list)
        warnings.warn("call not tested")
        return to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def get_separation_time_in_junction(self, preceding_train_path_node_id: int, succeeding_train_path_node_id: int) \
            -> datetime.timedelta:
        url_tail = 'junction-separation-time/between-train-path-nodes/{0}/{1}'.format(preceding_train_path_node_id,
                                                                                      succeeding_train_path_node_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return converter_helpers.parse_to_timedelta_or_None(response_dict["separationTime"])

    def get_station_track_reoccupation_separation_time(self, preceding_train_path_node_id: int,
                                                       succeeding_train_path_node_id: int, node_track_id: int
                                                       ) -> datetime.timedelta:
        url_tail = 'station-track-reoccupation-separation-time/{0}/{1}/{2}'.format(preceding_train_path_node_id,
                                                                                   succeeding_train_path_node_id,
                                                                                   node_track_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_separation_time_in_any_junction(self, preceding_train_path_node_id: int, succeeding_train_path_node_id: int,
                                            node_id: int, preceding_route_start_id: int, preceding_route_end_id: int,
                                            succeeding_route_start_id: int, succeeding_route_end_id: int) \
            -> datetime.timedelta:
        url_tail = ('junction-separation-time/between-train-path-nodes/{0}/{1}/for-node/{2}/preceding-route/{3}/{4}/' +
                    'succeeding-route/{5}/{6}').format(preceding_train_path_node_id, succeeding_train_path_node_id,
                                                       node_id, preceding_route_start_id, preceding_route_end_id,
                                                       succeeding_route_start_id, succeeding_route_end_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return converter_helpers.parse_to_timedelta_or_None(response_dict["separationTime"])

    def get_separation_time_in_station(self, preceding_section_track_id: int, preceding_node_track_id: int,
                                       preceding_stop_status: AIDM_enum_classes.StopStatus,
                                       succeeding_section_track_id: int, succeeding_node_track_id: int,
                                       succeeding_stop_status: AIDM_enum_classes.StopStatus) -> datetime.timedelta:
        url_tail = ('station-separation-time/from-section-track/{0}/to-node-track/{1}/{2}/from-section-track/{3}' +
                    '/to-node-track/{4}/{5}').format(preceding_section_track_id, preceding_node_track_id,
                                                     preceding_stop_status.name, succeeding_section_track_id,
                                                     succeeding_node_track_id, succeeding_stop_status.name)

        response_dict = self.__communication_layer.do_get_request(url_tail)
        return converter_helpers.parse_to_timedelta_or_None(response_dict["separationTime"])

    def get_separation_time_in_station_for_entry_or_exit(self, preceding_train_path_node_id: int,
                                                         preceding_node_track_id: int,
                                                         preceding_station_entry_or_exit: AIDM_enum_classes.StationEntryOrExit,
                                                         succeeding_train_path_node_id: int,
                                                         succeeding_node_track_id: int,
                                                         succeeding_station_entry_or_exit:
                                                         AIDM_enum_classes.StationEntryOrExit) -> datetime.timedelta:
        url_tail = "station-separation-time/" + \
                   "{0}/{1}/{2}/{3}/{4}/{5}".format(preceding_train_path_node_id, preceding_node_track_id,
                                                    preceding_station_entry_or_exit.name, succeeding_train_path_node_id,
                                                    succeeding_node_track_id, succeeding_station_entry_or_exit.name)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return converter_helpers.parse_to_timedelta_or_None(response_dict['separationTime'])

    def get_headway_time_for_train_path_nodes(self, preceding_train_path_node_id: int,
                                              succeeding_train_path_node_id: int) -> datetime.timedelta:
        url_tail = 'headway-times/between-train-path-nodes/{0}/{1}'.format(preceding_train_path_node_id,
                                                                           succeeding_train_path_node_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_headway_time_for_train_path_nodes_on_section_track(self, preceding_train_path_node_id: int,
                                                               succeeding_train_path_node_id: int,
                                                               section_track_id: int, from_node_id: int,
                                                               to_node_id: int) -> datetime.timedelta:
        url_tail = 'headway-times/between-train-path-nodes/{0}/{1}/for-section-track/{2}/in-direction/{3}/{4}'.format(
            preceding_train_path_node_id, succeeding_train_path_node_id, section_track_id, from_node_id, to_node_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return converter_helpers.parse_to_timedelta(response_dict["headwayTime"])

    def get_assignable_station_tracks_in_algorithm_node(self, nodeID: int, trainPathNodeId: int,
                                                        stopStatus: AIDM_enum_classes.StopStatus) -> list:
        url_tail = "assignable-station-tracks-in-algorithm-node"
        get_request_params = dict(NodeID=nodeID, TrainPathNodeID=trainPathNodeId, StopStatus=stopStatus.name)
        response_list = self.__communication_layer.do_get_request(url_tail, get_request_params)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(AIDM_classes.AlgorithmNodeTrack, response_list)

    def get_assignable_station_tracks_on_train_path_node(self, trainPathNodeId: int) -> list:
        url_tail = "assignable-station-tracks-on-train-path-node"
        get_request_params = dict(TrainPathNodeID=trainPathNodeId)
        response_list = self.__communication_layer.do_get_request(url_tail, get_request_params)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(AIDM_classes.AlgorithmNodeTrack, response_list)

    def assign_station_track(self, trainPathNodeId: int, stationTrackIDOrNone: (None, int) = None) -> \
            AIDM_classes.AlgorithmTrain:
        url_tail = "assign-station-track"
        post_request_body = dict(TrainPathNodeID=trainPathNodeId, NodeTrackID=str(stationTrackIDOrNone))
        response_dict = self.__communication_layer.do_post_request(url_tail, post_request_body)
        return to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def get_incoming_routing_edges(self, routing_point: AIDM_classes.RoutingPoint) \
            -> AIDM_classes.IncomingRoutingEdgeSet:
        url_tail = "nodes/{0}/incoming-routing-edges".format(routing_point.NodeID)
        get_request_params = extract_parameters_from_routing_point(routing_point)
        response_dict = self.__communication_layer.do_get_request(url_tail, get_request_params)
        # TODO complete testing after BugFix!
        return to_AIDM_converter.convert_dict_to_IncomingRoutingEdgeSet(response_dict)

    def get_outgoing_routing_edges(self, routing_point: AIDM_classes.RoutingPoint) \
            -> AIDM_classes.OutgoingRoutingEdgeSet:
        url_tail = "nodes/{0}/outgoing-routing-edges".format(routing_point.NodeID)
        get_request_params = extract_parameters_from_routing_point(routing_point)
        response_dict = self.__communication_layer.do_get_request(url_tail, get_request_params)
        # TODO complete testing after BugFix!
        return to_AIDM_converter.convert_dict_to_OutgoingRoutingEdgeSet(response_dict)

    def get_crossing_routing_edges(self, routing_point: AIDM_classes.RoutingPoint) -> \
            AIDM_classes.CrossingRoutingEdgeSet:
        url_tail = "nodes/{0}/incoming-routing-edges".format(routing_point.NodeID)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        # TODO complete testing after BugFix!
        return to_AIDM_converter.convert_dict_to_CrossingRoutingEdgeSet(response_dict)

    def get_formation(self, formation_id: int) -> AIDM_classes.AlgorithmFormation:
        url_tail = "vehicles/formations/{0}".format(formation_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return to_AIDM_converter.convert_dict_to_AIDM(AIDM_classes.AlgorithmFormation, response_dict)

    def get_vehicle_type(self, vehicle_type_id: int) -> AIDM_classes.AlgorithmVehicleType:
        url_tail = "vehicles/types/{0}".format(vehicle_type_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return to_AIDM_converter.convert_dict_to_AIDM(AIDM_classes.AlgorithmVehicleType, response_dict)

    def calculate_run_times(self, train_id: int) -> (AIDM_classes.UpdateTrainTimes, None):
        url_tail = "calculate-run-times/{0}".format(train_id)
        response_dict = self.__communication_layer.do_get_request(url_tail)
        return to_AIDM_converter.convert_dict_to_UpdateTrainTimes(response_dict)

    def __delegate_get_any_parameter(self, key: str) -> (bool, int, str, list, AIDM_classes.AlgorithmTrain,
                                                         AIDM_classes.TimeWindow):
        url_tail = "parameters/{0}".format(key)
        return self.__communication_layer.do_get_request(url_tail)["Value"]

    def get_bool_algorithm_parameter(self, key: str) -> bool:
        return self.__delegate_get_any_parameter(key)

    def get_int_algorithm_parameter(self, key: str) -> int:
        return self.__delegate_get_any_parameter(key)

    def get_string_algorithm_parameter(self, key: str) -> str:
        return self.__delegate_get_any_parameter(key)

    def get_algorithm_train_parameter(self, key: str) -> AIDM_classes.AlgorithmTrain:
        response_dict = self.__delegate_get_any_parameter(key)
        return to_AIDM_converter.convert_dict_to_AlgorithmTrain(response_dict)

    def get_algorithm_trains_parameter(self, key: str) -> list:
        response_list = self.__delegate_get_any_parameter(key)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(
            to_AIDM_converter.convert_dict_to_AlgorithmTrain, response_list)

    def get_time_window_algorithm_parameter(self, key: str) -> AIDM_classes.TimeWindow:
        response_dict = self.__delegate_get_any_parameter(key)
        return to_AIDM_converter.convert_dict_to_TimeWindow(response_dict)

    def get_node_track_closures(self, time_window: AIDM_classes.TimeWindow) -> list:
        time_window_dict = from_AIDM_converter.convert_to_json_conform_dict(time_window)
        url_tail = 'possessions/node-track-closures'
        response_dict = self.__communication_layer.do_get_request(url_tail, request_param=time_window_dict)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(
            to_AIDM_converter.convert_dict_to_AlgorithmNodeTrackClosure, response_dict)

    def get_section_track_closures(self, time_window: AIDM_classes.TimeWindow) -> list:
        time_window_dict = from_AIDM_converter.convert_to_json_conform_dict(time_window)
        url_tail = 'possessions/section-track-closures'
        response_list_of_dict = self.__communication_layer.do_get_request(url_tail, request_param=time_window_dict)
        return to_AIDM_converter.convert_list_of_dict_to_list_of_AIDM(
            to_AIDM_converter.convert_dict_to_AlgorithmSectionTrackClosure, response_list_of_dict)
