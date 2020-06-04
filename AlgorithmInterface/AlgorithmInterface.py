import datetime
import AIDMClasses
from AlgorithmInterface.AlgorithmInterfaceHelpers import merge_query_parameters, \
    create_query_parameters_from_preceding_and_succeeding_routing_edge
from typing import List, Optional, Union
from Communication import CommunicationLayer
from Conversion import converter_helpers, algorithm_platform_json_to_AIDM_converter, \
    object_to_algorithm_platform_json_converter


class AlgorithmInterface:
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

    def get_node(self, node_id: int) -> AIDMClasses.AlgorithmNode:
        url_to_resource = 'nodes/{0}'.format(node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNode(response_dict)

    def get_neighbor_nodes(self, node_id: int) -> List[AIDMClasses.AlgorithmNode]:
        url_to_resource = 'neighbor-nodes/{0}'.format(node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)

        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNode,
            response_list
        )

    def get_section_track(self, section_track_id: int) -> AIDMClasses.AlgorithmSectionTrack:
        url_to_resource = 'section-tracks/{0}'.format(section_track_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert(AIDMClasses.AlgorithmSectionTrack, response_dict)

    def get_directed_section_tracks(
            self,
            first_node_id: int,
            second_node_id: int
    ) -> List[AIDMClasses.AlgorithmSectionTrack]:
        url_to_resource = 'section-tracks-between/{0}/{1}'.format(first_node_id, second_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmSectionTrack, response_list)

    def get_parallel_section_tracks(self, section_track_id: int) -> List[AIDMClasses.AlgorithmSectionTrack]:
        url_to_resource = 'section-tracks-parallel-to/{0}'.format(section_track_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmSectionTrack, response_list)

    def get_train_classification(self, train_id: int) -> AIDMClasses.AlgorithmTrainClassification:
        url_to_resource = 'train-classification/{0}'.format(train_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert(AIDMClasses.AlgorithmTrainClassification, response_dict)

    def get_train_classifications(self) -> List[AIDMClasses.AlgorithmTrainClassification]:
        url_to_resource = 'train-classifications'
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmTrainClassification, response_list)

    def get_trains(self, timeWindow: AIDMClasses.TimeWindow) -> List[AIDMClasses.AlgorithmTrain]:
        url_to_resource = "trains"
        get_request_params = object_to_algorithm_platform_json_converter.convert_any_object(timeWindow)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters=get_request_params)

        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain,
            response_list
        )

    def get_trains_driving_any_node(
            self,
            timeWindow: AIDMClasses.TimeWindow,
            nodeIDs: List[int]
    ) -> List[AIDMClasses.AlgorithmTrain]:
        url_to_resource = "trains"
        manual_converted_query_parameters = dict(NodeFilter=nodeIDs)
        query_parameters = merge_query_parameters(
            [
                manual_converted_query_parameters,
                object_to_algorithm_platform_json_converter.convert_any_object(timeWindow)
            ]
        )
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters=query_parameters)
        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain,
            response_list
        )

    def get_trains_cut_to_time_range(self, timeWindow: AIDMClasses.TimeWindow) -> List[AIDMClasses.AlgorithmTrain]:
        url_to_resource = "trains"
        cut_train_query_parameters = dict(CutTrain=True)
        query_parameters = merge_query_parameters(
            [
                cut_train_query_parameters,
                object_to_algorithm_platform_json_converter.convert_any_object(timeWindow)
            ]
        )
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters=query_parameters)

        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain,
            response_list
        )

    def get_trains_cut_to_time_range_driving_any_node(
            self,
            timeWindow: AIDMClasses.TimeWindow,
            nodeIDs: List[int]
    ) -> List[AIDMClasses.AlgorithmTrain]:
        url_to_resource = "trains"
        manual_converted_query_parameters = dict(CutTrain=True, NodeFilter=nodeIDs)
        query_parameters = merge_query_parameters(
            [
                manual_converted_query_parameters,
                object_to_algorithm_platform_json_converter.convert_any_object(timeWindow)
            ]
        )
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters=query_parameters)

        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain,
            response_list
        )

    def cancel_train(self, train_id: int) -> int:
        url_to_resource = 'cancel-train'
        post_request_body = dict(trainID=train_id)
        return self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)

    def cancel_train_from(self, train_path_node_id: int) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = 'cancel-train-from'
        post_request_body = dict(trainPathNodeID=train_path_node_id)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def cancel_train_to(self, train_path_node_id: int) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = 'cancel-train-to'
        post_request_body = dict(trainPathNodeID=train_path_node_id)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def clone_train(self, train_id: int) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = 'clone-train'
        post_request_body = dict(TrainID=train_id)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def reroute_train(self, route: AIDMClasses.UpdateTrainRoute):
        url_to_resource = "reroute-train"
        post_request_body = object_to_algorithm_platform_json_converter.convert_any_object(route)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def set_section_track(self, train_path_node_id: int, section_track_id: int) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = 'set-section-track'
        post_request_body = dict(TrainPathNodeID=train_path_node_id, SectionTrackID=section_track_id)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body=post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def update_train_times(
            self,
            train_id: int,
            update_train_times_nodes: List[AIDMClasses.UpdateTrainTimesNode]
    ) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = 'trains/{0}/train-path-nodes'.format(train_id)
        put_body_list = object_to_algorithm_platform_json_converter.convert_any_object(update_train_times_nodes)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_list)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def update_trajectory(
            self,
            train_id: int,
            update_train_stop_times_node: AIDMClasses.UpdateTrainStopTimesNode
    ) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-trajectory-stop-times".format(train_id)
        put_body_list = object_to_algorithm_platform_json_converter.convert_any_object(update_train_stop_times_node)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_list)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def get_separation_time_in_junction_for_planned_train_paths(
            self,
            node_id: int,
            preceding_train_path_node_id: int,
            succeeding_train_path_node_id: int
    ) -> Optional[datetime.timedelta]:
        url_to_resource = 'nodes/{0}/separation-times'.format(node_id)
        query_parameters = dict(
            PrecedingTrainPathNodeID=preceding_train_path_node_id,
            SucceedingTrainPathNodeID=succeeding_train_path_node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta_or_None(response_dict["separationTime"])

    def get_separation_time_in_junction_for_routes(
            self,
            preceding_routing_edge: AIDMClasses.CrossingRoutingEdge,
            succeeding_routing_edge: AIDMClasses.CrossingRoutingEdge
    ) -> Optional[datetime.timedelta]:
        url_to_resource = 'nodes/{0}/separation-times'.format(preceding_routing_edge.NodeID)
        query_parameters = dict(
            PrecedingFromSectionTrackID=preceding_routing_edge.StartSectionTrackID,
            PrecedingToSectionTrackID=preceding_routing_edge.EndSectionTrackID,
            SucceedingFromSectionTrackID=succeeding_routing_edge.StartSectionTrackID,
            SucceedingToSectionTrackID=succeeding_routing_edge.EndSectionTrackID)

        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta_or_None(response_dict["separationTime"])

    def get_separation_time_in_station_for_node_track_reoccupation(
            self,
            node_id: int,
            node_track_id: int) -> datetime.timedelta:
        url_to_resource = 'nodes/{0}/separation-times'.format(node_id)
        query_parameters = dict(NodeTrackID=node_track_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_separation_time_in_station_for_planned_train_paths(
            self,
            node_id: int,
            preceding_train_path_node_id: int,
            preceding_train_stop_status: Optional[AIDMClasses.StopStatus],
            preceding_station_entry_or_exit: AIDMClasses.StationEntryOrExit,
            succeeding_train_path_node_id: int,
            succeeding_train_stop_status: Optional[AIDMClasses.StopStatus],
            succeeding_station_entry_or_exit: AIDMClasses.StationEntryOrExit
    ) -> Optional[datetime.timedelta]:

        url_to_resource = "nodes/{0}/separation-times".format(node_id)
        query_parameters = dict(
            PrecedingTrainPathNodeID=preceding_train_path_node_id,
            PrecedingEntryOrExit=preceding_station_entry_or_exit.name,
            SucceedingTrainPathNodeID=succeeding_train_path_node_id,
            SucceedingEntryOrExit=succeeding_station_entry_or_exit.name)

        if preceding_train_stop_status is not None:
            query_parameters['PrecedingStopStatus'] = preceding_train_stop_status.name
        if succeeding_train_stop_status is not None:
            query_parameters['SucceedingStopStatus'] = succeeding_train_stop_status.name

        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta_or_None(response_dict['separationTime'])

    def get_separation_time_in_station_for_routes(
            self,
            preceding_train_routing_edge: Union[AIDMClasses.IncomingRoutingEdge, AIDMClasses.OutgoingRoutingEdge],
            preceding_stop_status: AIDMClasses.StopStatus,
            succeeding_train_routing_edge: Union[AIDMClasses.IncomingRoutingEdge, AIDMClasses.OutgoingRoutingEdge],
            succeeding_stop_status: AIDMClasses.StopStatus
    ) -> Optional[datetime.timedelta]:

        url_to_resource = 'nodes/{0}/separation-times'.format(preceding_train_routing_edge.NodeID)
        query_parameters = create_query_parameters_from_preceding_and_succeeding_routing_edge(
            preceding_train_routing_edge,
            succeeding_train_routing_edge)
        query_parameters['PrecedingStopStatus'] = preceding_stop_status.name
        query_parameters['SucceedingStopStatus'] = succeeding_stop_status.name
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)

        return converter_helpers.parse_to_timedelta_or_None(response_dict["separationTime"])

    def get_default_headway_time(
            self,
            section_track_id: int,
            from_node_id: Optional[int],
            to_node_id: Optional[int]
    ) -> datetime.timedelta:

        url_to_resource = "section-tracks/{0}/headway-times".format(section_track_id)
        headway_query_parameters = dict()
        if from_node_id is not None:
            headway_query_parameters['FromNodeID'] = from_node_id
        if to_node_id is not None:
            headway_query_parameters['ToNodeID'] = to_node_id

        response_dict = self.__communication_layer.do_get_request(url_to_resource, headway_query_parameters)
        return converter_helpers.parse_to_timedelta(response_dict["headwayTime"])

    def get_headway_time(
            self,
            section_track_id: int,
            from_node_id: Optional[int],
            to_node_id: Optional[int],
            preceding_train_path_node_id: int,
            succeeding_train_path_node_id: int
    ) -> datetime.timedelta:

        url_to_resource = "section-tracks/{0}/headway-times".format(section_track_id)
        headway_query_parameters = dict(
            PrecedingTrainPathNodeID=preceding_train_path_node_id,
            SucceedingTrainPathNodeID=succeeding_train_path_node_id)
        if from_node_id is not None:
            headway_query_parameters['FromNodeID'] = from_node_id
        if to_node_id is not None:
            headway_query_parameters['ToNodeID'] = to_node_id

        response_dict = self.__communication_layer.do_get_request(url_to_resource, headway_query_parameters)
        return converter_helpers.parse_to_timedelta(response_dict["headwayTime"])

    def get_headway_time_for_train_path_nodes(
            self,
            preceding_train_path_node_id: int,
            succeeding_train_path_node_id: int
    ) -> datetime.timedelta:
        url_to_resource = 'headway-times/between-train-path-nodes/{0}/{1}'.format(
            preceding_train_path_node_id,
            succeeding_train_path_node_id
        )
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_headway_time_for_train_path_nodes_on_section_track(
            self,
            preceding_train_path_node_id: int,
            succeeding_train_path_node_id: int,
            section_track_id: int,
            from_node_id: int,
            to_node_id: int
    ) -> datetime.timedelta:
        url_to_resource = 'headway-times/between-train-path-nodes/{0}/{1}/for-section-track/{2}/' \
                          'in-direction/{3}/{4}'.format(
            preceding_train_path_node_id,
            succeeding_train_path_node_id,
            section_track_id,
            from_node_id,
            to_node_id
        )
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta(response_dict["headwayTime"])

    def get_assignable_station_tracks_in_algorithm_node(
            self,
            nodeID: int,
            trainPathNodeId: int,
            stopStatus: AIDMClasses.StopStatus
    ) -> List[AIDMClasses.AlgorithmNodeTrack]:
        url_to_resource = "assignable-station-tracks-in-algorithm-node"
        get_request_params = dict(NodeID=nodeID, TrainPathNodeID=trainPathNodeId, StopStatus=stopStatus.name)
        response_list = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmNodeTrack, response_list)

    def get_assignable_station_tracks_on_train_path_node(
            self,
            trainPathNodeId: int
    ) -> List[AIDMClasses.AlgorithmNodeTrack]:
        url_to_resource = "assignable-station-tracks-on-train-path-node"
        get_request_params = dict(TrainPathNodeID=trainPathNodeId)
        response_list = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmNodeTrack, response_list)

    def assign_station_track(
            self,
            trainPathNodeId: int,
            stationTrackIDOrNone: Optional[int] = None
    ) -> AIDMClasses.AlgorithmTrain:
        url_to_resource = "assign-station-track"
        post_request_body = dict(TrainPathNodeID=trainPathNodeId, NodeTrackID=str(stationTrackIDOrNone))
        response_dict = self.__communication_layer.do_post_request(url_to_resource, post_request_body)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain(response_dict)

    def get_incoming_routing_edges(self, routing_point: AIDMClasses.RoutingPoint) -> AIDMClasses.IncomingRoutingEdgeSet:
        url_to_resource = "nodes/{0}/incoming-routing-edges".format(routing_point.NodeID)
        if routing_point.NodeTrackID is not None:
            get_request_params = dict(EndNodeTrackID=routing_point.NodeTrackID)
        else:
            get_request_params = dict()
        response_dict = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_IncomingRoutingEdgeSet(response_dict)

    def get_outgoing_routing_edges(self, routing_point: AIDMClasses.RoutingPoint) -> AIDMClasses.OutgoingRoutingEdgeSet:
        url_to_resource = "nodes/{0}/outgoing-routing-edges".format(routing_point.NodeID)
        if routing_point.NodeTrackID is not None:
            get_request_params = dict(StartNodeTrackID=routing_point.NodeTrackID)
        else:
            get_request_params = dict()
        response_dict = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_OutgoingRoutingEdgeSet(response_dict)

    def get_crossing_routing_edges(self, routing_point: AIDMClasses.RoutingPoint) -> AIDMClasses.CrossingRoutingEdgeSet:
        url_to_resource = "nodes/{0}/crossing-routing-edges".format(routing_point.NodeID)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_CrossingRoutingEdgeSet(response_dict)

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
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_UpdateTrainTimes(response_dict)

    def notify_user(self, message_level_1: str, message_level_2: str) -> None:
        url_to_resource = 'notifications'
        request_body = dict(messageLevel1=message_level_1, messageLevel2=message_level_2)
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def show_status_message(self, short_message: str, long_message: Optional[str] = None) -> None:
        url_to_resource = 'status-message'
        request_body = dict(shortMessage=short_message, longMessage=long_message)
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def __delegate_get_any_parameter(
            self,
            key: str
    ) -> Union[
        AIDMClasses.AlgorithmTrain,
        AIDMClasses.TimeWindow,
        bool,
        int,
        str,
        list,
        dict
    ]:
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

    def get_algorithm_trains_parameter(self, key: str) -> List[AIDMClasses.AlgorithmTrain]:
        response_list = self.__delegate_get_any_parameter(key)

        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmTrain,
            response_list
        )

    def get_time_window_algorithm_parameter(self, key: str) -> AIDMClasses.TimeWindow:
        response_dict = self.__delegate_get_any_parameter(key)
        return algorithm_platform_json_to_AIDM_converter.convert_json_to_TimeWindow(response_dict)

    def get_node_track_closures(
            self,
            time_window: AIDMClasses.TimeWindow
    ) -> List[AIDMClasses.AlgorithmNodeTrackClosure]:
        url_to_resource = 'possessions/node-track-closures'
        get_request_params = object_to_algorithm_platform_json_converter.convert_any_object(time_window)
        response_list_of_dict = self.__communication_layer.do_get_request(
            url_to_resource,
            query_parameters=get_request_params
        )

        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNodeTrackClosure,
            response_list_of_dict
        )

    def get_section_track_closures(
            self,
            time_window: AIDMClasses.TimeWindow
    ) -> List[AIDMClasses.AlgorithmSectionTrackClosure]:
        get_request_params = object_to_algorithm_platform_json_converter.convert_any_object(time_window)
        url_to_resource = 'possessions/section-track-closures'
        response_list_of_dict = self.__communication_layer.do_get_request(
            url_to_resource,
            query_parameters=get_request_params
        )

        return algorithm_platform_json_to_AIDM_converter.convert_list(
            algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmSectionTrackClosure,
            response_list_of_dict
        )
