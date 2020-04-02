__version__ = '0.0.1'
__author__ = 'Florian Fuchs'

import datetime
import AIDMClasses
import AIDMClasses.AIDM_RoutingEdge_classes

from AlgorithmInterface.AlgorithmInterfaceHelpers import extract_parameters_from_routing_point, \
    add_cut_train_to_get_request_params, add_node_filter_to_get_request_params
from Communication import CommunicationLayer
from Conversion import converter_helpers, algorithm_platform_json_to_AIDM_converter, \
    object_to_algorithm_platform_json_converter


class AlgorithmicPlatformInterface:
    __communication_layer: CommunicationLayer.CommunicationLayer

    def __init__(self, base_url: str):
        self.__communication_layer = CommunicationLayer.CommunicationLayer(base_url)

    def __enter__(self):
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.__communication_layer.currentSession.close()

    @property
    def base_url(self) -> str:
        return self.__communication_layer.base_url

    def notify_user(self, message_level_1: str, message_level_2: str) -> None:
        url_to_resource = 'notifications'
        request_body = {'messageLevel1': message_level_1, 'messageLevel2': message_level_2}
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def show_status_message(self, short_message: str, long_message: (str, None) = None) -> None:
        url_to_resource = 'status-message'
        request_body = {'shortMessage': short_message, 'longMessage': long_message}
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def get_node(self, node_id: int) -> AIDMClasses.AlgorithmNode:
        url_to_resource = 'nodes/{0}'.format(node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_dict_to_AlgorithmNode(response_dict)

    def get_neighbor_nodes(self, node_id: int) -> list:
        url_to_resource = 'neighbor-nodes/{0}'.format(node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_dict_to_AlgorithmNode, response_list)

    def get_section_track(self, section_track_id: int) -> AIDMClasses.AlgorithmSectionTrack:
        url_to_resource = 'section-tracks/{0}'.format(section_track_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert(AIDMClasses.AlgorithmSectionTrack, response_dict)

    def get_directed_section_tracks(self, first_node_id: int, second_node_id: int) -> list:
        url_to_resource = 'section-tracks-between/{0}/{1}'.format(first_node_id, second_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmSectionTrack, response_list)

    def get_parallel_section_tracks(self, section_track_id: int) -> list:
        url_to_resource = 'section-tracks-parallel-to/{0}'.format(section_track_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmSectionTrack, response_list)

    def get_train_classification(self, train_id: int) -> dict:
        url_to_resource = 'train-classification/{0}'.format(train_id)
        return self.__communication_layer.do_get_request(url_to_resource)

    def get_train_classifications(self) -> dict:
        url_to_resource = 'train-classifications'
        return self.__communication_layer.do_get_request(url_to_resource)

    def get_trains(self, timeWindow: AIDMClasses.TimeWindow) -> list:
        url_to_resource = "trains"
        get_request_params = object_to_algorithm_platform_json_converter.convert_any_object(timeWindow)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_param=get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain, response_list)

    def get_trains_driving_any_node(self, timeWindow: AIDMClasses.TimeWindow, nodeIDs: list) -> list:
        url_to_resource = "trains"
        part_of_get_request_params = object_to_algorithm_platform_json_converter.convert_any_object(timeWindow)
        get_request_params = add_node_filter_to_get_request_params(part_of_get_request_params, nodeIDs)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_param=get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain, response_list)

    def get_trains_cut_to_time_range(self, timeWindow: AIDMClasses.TimeWindow) -> list:
        url_to_resource = "trains"
        part_of_get_request_params = object_to_algorithm_platform_json_converter.convert_any_object(timeWindow)
        get_request_params = add_cut_train_to_get_request_params(part_of_get_request_params)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_param=get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain, response_list)

    def get_trains_cut_to_time_range_driving_any_node(self, timeWindow: AIDMClasses.TimeWindow, nodeIDs: list) -> list:
        url_to_resource = "trains"
        get_request_params = object_to_algorithm_platform_json_converter.convert_any_object(timeWindow)
        get_request_params = add_node_filter_to_get_request_params(get_request_params, nodeIDs)
        get_request_params = add_cut_train_to_get_request_params(get_request_params)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_param=get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain, response_list)

    def cancel_train(self, train_id: int) -> int:
        url_to_resource = 'cancel-train'
        post_request_body = {'trainID': train_id}
        return self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)

    def cancel_train_from(self, train_path_node_id: int) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = 'cancel-train-from'
        post_request_body = {'trainPathNodeID': train_path_node_id}
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def cancel_train_to(self, train_path_node_id: int) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = 'cancel-train-to'
        post_request_body = {'trainPathNodeID': train_path_node_id}
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def clone_train(self, train_id: int) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = 'clone-train'
        post_request_body = {'TrainID': train_id}
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def reroute_train(self, route: AIDMClasses.UpdateTrainRoute):
        url_to_resource = "reroute-train"
        post_request_body = object_to_algorithm_platform_json_converter.convert_any_object(route)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def set_section_track(self, train_path_node_id: int, section_track_id: int) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = 'set-section-track'
        post_request_body = {'TrainPathNodeID': train_path_node_id, 'SectionTrackID': section_track_id}
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def update_train_times(self, train_id: int, update_train_times_nodes: list) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = 'trains/{0}/train-path-nodes'.format(train_id)
        put_body_list = object_to_algorithm_platform_json_converter.convert_any_object(update_train_times_nodes)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_list)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def update_trajectory(self, train_id: int, update_train_stop_times_nodes: list) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-trajectory-stop-times".format(train_id)
        put_body_list = object_to_algorithm_platform_json_converter.convert_any_object(update_train_stop_times_nodes)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_list)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def get_separation_time_in_junction(self, preceding_train_path_node_id: int, succeeding_train_path_node_id: int) \
            -> datetime.timedelta:
        url_to_resource = 'junction-separation-time/between-train-path-nodes/{0}/{1}'.format(
            preceding_train_path_node_id,
            succeeding_train_path_node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta_or_None(response_dict["separationTime"])

    def get_station_track_reoccupation_separation_time(self, preceding_train_path_node_id: int,
                                                       succeeding_train_path_node_id: int, node_track_id: int
                                                       ) -> datetime.timedelta:
        url_to_resource = 'station-track-reoccupation-separation-time/{0}/{1}/{2}'.format(preceding_train_path_node_id,
                                                                                          succeeding_train_path_node_id,
                                                                                          node_track_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_separation_time_in_any_junction(self, preceding_train_path_node_id: int, succeeding_train_path_node_id: int,
                                            node_id: int, preceding_route_start_id: int, preceding_route_end_id: int,
                                            succeeding_route_start_id: int, succeeding_route_end_id: int) \
            -> datetime.timedelta:
        url_to_resource = ('junction-separation-time/between-train-path-nodes/{0}/{1}/for-node/{2}/' +
                           'preceding-route/{3}/{4}/succeeding-route/{5}/{6}').format(preceding_train_path_node_id,
                                                                                      succeeding_train_path_node_id,
                                                                                      node_id, preceding_route_start_id,
                                                                                      preceding_route_end_id,
                                                                                      succeeding_route_start_id,
                                                                                      succeeding_route_end_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta_or_None(response_dict["separationTime"])

    def get_separation_time_in_station(self, preceding_section_track_id: int, preceding_node_track_id: int,
                                       preceding_stop_status: AIDMClasses.StopStatus,
                                       succeeding_section_track_id: int, succeeding_node_track_id: int,
                                       succeeding_stop_status: AIDMClasses.StopStatus) -> datetime.timedelta:
        url_to_resource = ('station-separation-time/from-section-track/{0}/to-node-track/{1}/{2}'
                           + '/from-section-track/{3}/to-node-track/{4}/{5}').format(preceding_section_track_id,
                                                                                     preceding_node_track_id,
                                                                                     preceding_stop_status.name,
                                                                                     succeeding_section_track_id,
                                                                                     succeeding_node_track_id,
                                                                                     succeeding_stop_status.name)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta_or_None(response_dict["separationTime"])

    def get_separation_time_in_station_for_entry_or_exit(self, preceding_train_path_node_id: int,
                                                         preceding_node_track_id: int,
                                                         preceding_station_entry_or_exit: AIDMClasses.StationEntryOrExit,
                                                         succeeding_train_path_node_id: int,
                                                         succeeding_node_track_id: int,
                                                         succeeding_station_entry_or_exit:
                                                         AIDMClasses.StationEntryOrExit) -> datetime.timedelta:
        url_to_resource = "station-separation-time/" + \
                          "{0}/{1}/{2}/{3}/{4}/{5}".format(preceding_train_path_node_id, preceding_node_track_id,
                                                           preceding_station_entry_or_exit.name,
                                                           succeeding_train_path_node_id,
                                                           succeeding_node_track_id,
                                                           succeeding_station_entry_or_exit.name)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta_or_None(response_dict['separationTime'])

    def get_headway_time_for_train_path_nodes(self, preceding_train_path_node_id: int,
                                              succeeding_train_path_node_id: int) -> datetime.timedelta:
        url_to_resource = 'headway-times/between-train-path-nodes/{0}/{1}'.format(preceding_train_path_node_id,
                                                                                  succeeding_train_path_node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_headway_time_for_train_path_nodes_on_section_track(self, preceding_train_path_node_id: int,
                                                               succeeding_train_path_node_id: int,
                                                               section_track_id: int, from_node_id: int,
                                                               to_node_id: int) -> datetime.timedelta:
        url_to_resource = ('headway-times/between-train-path-nodes/{0}/{1}/for-section-track/{2}/' +
                           'in-direction/{3}/{4}').format(preceding_train_path_node_id, succeeding_train_path_node_id,
                                                          section_track_id, from_node_id, to_node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta(response_dict["headwayTime"])

    def get_assignable_station_tracks_in_algorithm_node(self, nodeID: int, trainPathNodeId: int,
                                                        stopStatus: AIDMClasses.StopStatus) -> list:
        url_to_resource = "assignable-station-tracks-in-algorithm-node"
        get_request_params = dict(NodeID=nodeID, TrainPathNodeID=trainPathNodeId, StopStatus=stopStatus.name)
        response_list = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmNodeTrack, response_list)

    def get_assignable_station_tracks_on_train_path_node(self, trainPathNodeId: int) -> list:
        url_to_resource = "assignable-station-tracks-on-train-path-node"
        get_request_params = dict(TrainPathNodeID=trainPathNodeId)
        response_list = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmNodeTrack, response_list)

    def assign_station_track(self, trainPathNodeId: int, stationTrackIDOrNone: (None, int) = None) -> \
            AIDMClasses.AlgorithmTrain:
        url_to_resource = "assign-station-track"
        post_request_body = dict(TrainPathNodeID=trainPathNodeId, NodeTrackID=str(stationTrackIDOrNone))
        response_dict = self.__communication_layer.do_post_request(url_to_resource, post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def get_incoming_routing_edges(self, routing_point: AIDMClasses.RoutingPoint) \
            -> AIDMClasses.AIDM_RoutingEdge_classes.IncomingRoutingEdgeSet:
        url_to_resource = "nodes/{0}/incoming-routing-edges".format(routing_point.NodeID)
        get_request_params = extract_parameters_from_routing_point(routing_point)
        response_dict = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_dict_to_IncomingRoutingEdgeSet(response_dict)

    def get_outgoing_routing_edges(self, routing_point: AIDMClasses.RoutingPoint) \
            -> AIDMClasses.AIDM_RoutingEdge_classes.OutgoingRoutingEdgeSet:
        url_to_resource = "nodes/{0}/outgoing-routing-edges".format(routing_point.NodeID)
        get_request_params = extract_parameters_from_routing_point(routing_point)
        response_dict = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_dict_to_OutgoingRoutingEdgeSet(response_dict)

    def get_crossing_routing_edges(self, routing_point: AIDMClasses.RoutingPoint) -> \
            AIDMClasses.AIDM_RoutingEdge_classes.CrossingRoutingEdgeSet:
        url_to_resource = "nodes/{0}/crossing-routing-edges".format(routing_point.NodeID)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_dict_to_CrossingRoutingEdgeSet(response_dict)

    def get_formation(self, formation_id: int) -> AIDMClasses.AlgorithmFormation:
        url_to_resource = "vehicles/formations/{0}".format(formation_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert(AIDMClasses.AlgorithmFormation, response_dict)

    def get_vehicle_type(self, vehicle_type_id: int) -> AIDMClasses.AlgorithmVehicleType:
        url_to_resource = "vehicles/types/{0}".format(vehicle_type_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert(AIDMClasses.AlgorithmVehicleType, response_dict)

    def calculate_run_times(self, train_id: int) -> (AIDMClasses.UpdateTrainTimes, None):
        url_to_resource = "calculate-run-times/{0}".format(train_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_dict_to_UpdateTrainTimes(response_dict)

    def __delegate_get_any_parameter(self, key: str) -> (bool, int, str, list, AIDMClasses.AlgorithmTrain,
                                                         AIDMClasses.TimeWindow):
        url_to_resource = "parameters/{0}".format(key)
        return self.__communication_layer.do_get_request(url_to_resource)["Value"]

    def get_bool_algorithm_parameter(self, key: str) -> bool:
        return self.__delegate_get_any_parameter(key)

    def get_int_algorithm_parameter(self, key: str) -> int:
        return self.__delegate_get_any_parameter(key)

    def get_string_algorithm_parameter(self, key: str) -> str:
        return self.__delegate_get_any_parameter(key)

    def get_algorithm_train_parameter(self, key: str) -> AIDMClasses.AlgorithmTrain:
        response_dict = self.__delegate_get_any_parameter(key)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def get_algorithm_trains_parameter(self, key: str) -> list:
        response_list = self.__delegate_get_any_parameter(key)
        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain, response_list)

    def get_time_window_algorithm_parameter(self, key: str) -> AIDMClasses.TimeWindow:
        response_dict = self.__delegate_get_any_parameter(key)
        return algorithm_platform_json_to_AIDM_converter.convert_dict_to_TimeWindow(response_dict)

    def get_node_track_closures(self, time_window: AIDMClasses.TimeWindow) -> list:
        url_to_resource = 'possessions/node-track-closures'
        get_request_params = object_to_algorithm_platform_json_converter.convert_any_object(time_window)
        response_dict = self.__communication_layer.do_get_request(url_to_resource, request_param=get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_dict_to_AlgorithmNodeTrackClosure, response_dict)

    def get_section_track_closures(self, time_window: AIDMClasses.TimeWindow) -> list:
        get_request_params = object_to_algorithm_platform_json_converter.convert_any_object(time_window)
        url_to_resource = 'possessions/section-track-closures'
        response_list_of_dict = self.__communication_layer.do_get_request(url_to_resource,
                                                                          request_param=get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_dict_to_AlgorithmSectionTrackClosure,
            response_list_of_dict)
