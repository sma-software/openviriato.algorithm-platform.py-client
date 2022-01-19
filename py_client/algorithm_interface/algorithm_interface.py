import datetime
from typing import Type, List, Optional, Union

from multipledispatch import dispatch

import py_client.algorithm_interface._algorithm_interface_helpers as _interface_helpers
import py_client.conversion.algorithm_platform_json_to_aidm_converter as from_json_converter
import py_client.conversion.converter_helpers as converter_helpers
import py_client.conversion.object_to_algorithm_platform_json_converter as to_json_converter
from py_client.aidm import (
    AlgorithmNode,
    RoutingEdgePair,
    AlgorithmSectionTrack,
    AlgorithmTrain,
    TimeWindow,
    AlgorithmTrainClassification,
    UpdateStopTimesTrainPathNode,
    UpdateTimesTrainPathNode,
    AnyRoutingEdgeIncomingOrOutgoing,
    StopStatus,
    RoutingPoint,
    IncomingNodeTrackRoutingEdge,
    OutgoingNodeTrackRoutingEdge,
    CrossingRoutingEdge,
    AnyRoutingEdgeIncomingOrCrossingOrOutgoing,
    StationEntryOrExit,
    UpdateTrainRoute,
    AlgorithmVehicleType,
    AlgorithmFormation,
    AlgorithmConnectionLink,
    AlgorithmAwaitArrivalLink,
    AlgorithmRosterLink,
    LinkType,
    AlgorithmNodeTrack,
    UpdateRunTimesTrainPathSegment,
    TerminationRequest,
    SignalType,
    TableRow,
    Maybe,
    FloatingPoint,
    UpdateTimesTrain,
    AlgorithmRosterLinkDefinition,
    TableDefinition,
    AlgorithmNodeTrackClosure,
    AlgorithmSectionTrackClosure,
    AlgorithmSectionRunningTimePenalty,
    AlgorithmTrainSimulationTrain,
    AlgorithmTrainSimulationEvent,
    AlgorithmMovementType,
    RunningTimePenaltyOnTrainPath,
    AlgorithmConflict
)
from py_client.communication.communication_layer import CommunicationLayer
from py_client.conversion.json_to_aidm_converter import JsonToAidmConverter


class AlgorithmInterface:
    __communication_layer: CommunicationLayer
    __json_to_aidm_converter: JsonToAidmConverter

    def __init__(self, base_url: str):
        self.__communication_layer = CommunicationLayer(base_url)
        self.__json_to_aidm_converter = JsonToAidmConverter()

    def __enter__(self):
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.__communication_layer.currentSession.close()

    @property
    def base_url(self) -> str:
        return self.__communication_layer.base_url

    def get_all_nodes(self) -> List[AlgorithmNode]:
        url_to_resource = "nodes"
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_node, response_list)

    def get_node(self, node_id: int) -> AlgorithmNode:
        url_to_resource = "nodes/{0}".format(node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_json_to_algorithm_node(response_dict)

    def get_preferred_routes_for_node(
        self,
        node_id: int,
        start_section_track_id: Optional[int],
        end_section_track_id: Optional[int],
    ) -> List[RoutingEdgePair]:
        url_to_resource = "nodes/{0}/preferred-routes".format(node_id)
        query_parameters = dict(startSectionTrackID=start_section_track_id, endSectionTrackID=end_section_track_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_to_routing_edge_pair, response_list)

    def get_preferred_routes_through_node(
        self,
        node_id: int,
        start_section_track_id: Optional[int],
        end_section_track_id: Optional[int],
    ) -> List[RoutingEdgePair]:
        url_to_resource = "nodes/{0}/preferred-routes".format(node_id)
        query_parameters = dict(
            startSectionTrackID=start_section_track_id,
            endSectionTrackID=end_section_track_id,
            endInNode=False,
            startInNode=False,
        )
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_to_routing_edge_pair, response_list)

    def get_preferred_starting_routes_for_node(
        self, node_id: int, end_section_track_id: Optional[int]
    ) -> List[RoutingEdgePair]:
        url_to_resource = "nodes/{0}/preferred-routes".format(node_id)
        query_parameters = dict(endSectionTrackID=end_section_track_id, endInNode=False, startInNode=True)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_to_routing_edge_pair, response_list)

    def get_preferred_ending_routes_for_node(
        self, node_id: int, start_section_track_id: Optional[int]
    ) -> List[RoutingEdgePair]:
        url_to_resource = "nodes/{0}/preferred-routes".format(node_id)
        query_parameters = dict(startSectionTrackID=start_section_track_id, endInNode=True, startInNode=False)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_to_routing_edge_pair, response_list)

    def get_all_section_tracks(self) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks"
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_section_track(self, section_track_id: int) -> AlgorithmSectionTrack:
        url_to_resource = "section-tracks/{0}".format(section_track_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return self.__json_to_aidm_converter.process_json_to_aidm(response_dict, AlgorithmSectionTrack)

    def get_nodes_with_section_track_from(self, from_node_id: int) -> List[AlgorithmNode]:
        url_to_resource = "nodes"
        query_parameters = dict(hasSectionTrackFromNodeId=from_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_node, response_list)

    def get_nodes_with_section_track_to(self, to_node_id: int) -> List[AlgorithmNode]:
        url_to_resource = "nodes"
        query_parameters = dict(hasSectionTrackToNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_node, response_list)

    def get_neighboring_nodes_between(self, from_node_id: int, to_node_id: int) -> List[AlgorithmNode]:
        url_to_resource = "nodes"
        query_parameters = dict(hasSectionTrackFromNodeId=from_node_id, hasSectionTrackToNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_node, response_list)

    def get_section_tracks_from(self, from_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks"
        query_parameters = dict(fromNodeId=from_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_section_tracks_to(self, to_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks"
        query_parameters = dict(toNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_section_tracks_between(self, from_node_id: int, to_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks"
        query_parameters = dict(fromNodeId=from_node_id, toNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_parallel_section_tracks(self, section_track_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks"
        query_parameters = dict(parallelToSectionTrackId=section_track_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_directed_section_tracks(self, first_node_id: int, second_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks-between/{0}/{1}".format(first_node_id, second_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_neighbor_nodes(self, node_id: int) -> List[AlgorithmNode]:
        url_to_resource = "neighbor-nodes/{0}".format(node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)

        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_node, response_list)

    def get_train_classification(self, train_id: int) -> AlgorithmTrainClassification:
        url_to_resource = "train-classifications/{0}".format(train_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert(AlgorithmTrainClassification, response_dict)

    def get_train_classifications(self) -> List[AlgorithmTrainClassification]:
        url_to_resource = "train-classifications"
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_list(AlgorithmTrainClassification, response_list)

    def get_trains(self, time_window: TimeWindow) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        query_parameters = to_json_converter.convert_any_object(time_window)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_train, response_list)

    def get_trains_driving_any_node(self, time_window: TimeWindow, node_ids: List[int]) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        manual_converted_query_parameters = dict(nodeFilter=node_ids)
        query_parameters = _interface_helpers.merge_query_parameters(
            [manual_converted_query_parameters, to_json_converter.convert_any_object(time_window)]
        )
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters=query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_train, response_list)

    def get_trains_cut_to_time_range(self, time_window: TimeWindow) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        cut_train_query_parameters = dict(cutTrain=True)
        query_parameters = _interface_helpers.merge_query_parameters(
            [cut_train_query_parameters, to_json_converter.convert_any_object(time_window)]
        )
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters=query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_train, response_list)

    def get_trains_cut_to_time_range_driving_any_node(
        self, time_window: TimeWindow, node_ids: List[int]
    ) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        manual_converted_query_parameters = dict(cutTrain=True, nodeFilter=node_ids)
        query_parameters = _interface_helpers.merge_query_parameters(
            [manual_converted_query_parameters, to_json_converter.convert_any_object(time_window)]
        )
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters=query_parameters)
        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_train, response_list)

    def update_train_formation(
        self,
        formation_id: int,
        train_id: int,
        from_train_path_node_id: int,
        to_train_path_node_id: Optional[int] = None,
    ) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-formation".format(train_id)
        manually_converted_put_body = dict(
            formationID=formation_id,
            fromTrainPathNodeID=from_train_path_node_id,
            toTrainPathNodeID=to_train_path_node_id,
        )
        response_dict = self.__communication_layer.do_put_request(url_to_resource, manually_converted_put_body)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def cancel_train(self, train_id: int) -> None:
        url_to_resource = "trains/{0}:cancel".format(train_id)
        self.__communication_layer.do_delete_request(url_to_resource)

    def update_movement_type(self, movement_type_id: int, train_id: int, from_train_path_node_id: int, to_train_path_node_id: int) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-movement-type".format(train_id)
        put_body_dict = dict(movementTypeId = movement_type_id,
                             fromTrainPathNodeId = from_train_path_node_id,
                             toTrainPathNodeId = to_train_path_node_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_dict)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def cancel_train_after(self, train_id: int, train_path_node_id: int) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes/{1}:cancel-after".format(train_id, train_path_node_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def cancel_train_before(self, train_id: int, train_path_node_id: int) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes/{1}:cancel-before".format(train_id, train_path_node_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def copy_train(self, train_id: int) -> AlgorithmTrain:
        url_to_resource = "trains/{0}:copy".format(train_id)
        response_dict = self.__communication_layer.do_post_request(url_to_resource)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def copy_train_and_replace_route(self, train_id: int, node_ids: List[int]):
        url_to_resource = "trains/{0}:copy-and-replace-route".format(train_id)
        post_request_body = dict(routeViaNodeIds=node_ids)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, post_request_body)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def reroute_train(self, train_id: int, route: UpdateTrainRoute):
        url_to_resource = "trains/{0}/train-path-nodes:reroute".format(train_id)
        put_request_body = to_json_converter.convert_any_object(route)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_request_body)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def update_section_track(self, train_id: int, train_path_node_id: int, section_track_id: int) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes/{1}:update-section-track".format(train_id, train_path_node_id)
        put_request_body = dict(sectionTrackId=section_track_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_request_body)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def update_train_times(
        self, train_id: int, update_train_times_nodes: List[UpdateTimesTrainPathNode]
    ) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-times".format(train_id)
        put_body_list = to_json_converter.convert_any_object(update_train_times_nodes)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_list)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    @dispatch(int, UpdateStopTimesTrainPathNode)
    def update_train_trajectory_stop_times(
        self, train_id: int, update_train_stop_times_node: UpdateStopTimesTrainPathNode
    ) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-trajectory-stop-times".format(train_id)
        put_body_list = to_json_converter.convert_any_object(update_train_stop_times_node)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_list)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    @dispatch(int, UpdateRunTimesTrainPathSegment)
    def update_train_trajectory_run_times(
        self,
        train_id: int,
        update_run_times_train_path_segment: UpdateRunTimesTrainPathSegment,
    ) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-trajectory-run-times".format(train_id)
        put_body_dict = to_json_converter.convert_any_object(update_run_times_train_path_segment)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_dict)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def get_separation_time_in_junction_for_planned_train_paths(
        self,
        node_id: int,
        preceding_train_path_node_id: int,
        succeeding_train_path_node_id: int,
    ) -> Optional[datetime.timedelta]:
        url_to_resource = "nodes/{0}/separation-times".format(node_id)
        query_parameters = dict(
            precedingTrainPathNodeId=preceding_train_path_node_id,
            succeedingTrainPathNodeId=succeeding_train_path_node_id,
        )
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta_or_none(response_dict["separationTime"])

    def get_separation_time_in_junction_for_routes(
        self,
        preceding_routing_edge: CrossingRoutingEdge,
        succeeding_routing_edge: CrossingRoutingEdge,
    ) -> Optional[datetime.timedelta]:
        url_to_resource = "nodes/{0}/separation-times".format(preceding_routing_edge.node_id)
        query_parameters = dict(
            precedingFromSectionTrackId=preceding_routing_edge.start_section_track_id,
            precedingToSectionTrackId=preceding_routing_edge.end_section_track_id,
            succeedingFromSectionTrackId=succeeding_routing_edge.start_section_track_id,
            succeedingToSectionTrackId=succeeding_routing_edge.end_section_track_id,
        )

        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta_or_none(response_dict["separationTime"])

    def get_separation_time_in_station_for_node_track_reoccupation(
        self, node_id: int, node_track_id: int
    ) -> datetime.timedelta:
        url_to_resource = "nodes/{0}/separation-times".format(node_id)
        query_parameters = dict(nodeTrackId=node_track_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_separation_time_in_station_for_planned_train_paths(
        self,
        node_id: int,
        preceding_train_path_node_id: int,
        preceding_train_stop_status: Optional[StopStatus],
        preceding_station_entry_or_exit: StationEntryOrExit,
        succeeding_train_path_node_id: int,
        succeeding_train_stop_status: Optional[StopStatus],
        succeeding_station_entry_or_exit: StationEntryOrExit,
    ) -> Optional[datetime.timedelta]:
        url_to_resource = "nodes/{0}/separation-times".format(node_id)

        query_parameters = dict(
            precedingTrainPathNodeId=preceding_train_path_node_id,
            precedingEntryOrExit=preceding_station_entry_or_exit.value,
            succeedingTrainPathNodeId=succeeding_train_path_node_id,
            succeedingEntryOrExit=succeeding_station_entry_or_exit.value,
        )

        if preceding_train_stop_status is not None:
            query_parameters["precedingStopStatus"] = preceding_train_stop_status.value
        if succeeding_train_stop_status is not None:
            query_parameters["succeedingStopStatus"] = succeeding_train_stop_status.value

        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta_or_none(response_dict["separationTime"])

    def get_separation_time_in_station_for_routes(
        self,
        preceding_train_routing_edge: AnyRoutingEdgeIncomingOrOutgoing,
        preceding_stop_status: StopStatus,
        succeeding_train_routing_edge: AnyRoutingEdgeIncomingOrOutgoing,
        succeeding_stop_status: StopStatus,
    ) -> Optional[datetime.timedelta]:
        url_to_resource = "nodes/{0}/separation-times".format(preceding_train_routing_edge.node_id)
        query_parameters = _interface_helpers.create_query_parameters_from_preceding_and_succeeding_routing_edge(
            preceding_train_routing_edge, succeeding_train_routing_edge
        )
        query_parameters["precedingStopStatus"] = preceding_stop_status.value
        query_parameters["succeedingStopStatus"] = succeeding_stop_status.value

        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)

        return converter_helpers.parse_to_timedelta_or_none(response_dict["separationTime"])

    def get_default_headway_time(
        self, section_track_id: int, from_node_id: Optional[int], to_node_id: Optional[int]
    ) -> datetime.timedelta:
        url_to_resource = "section-tracks/{0}/headway-times".format(section_track_id)
        headway_query_parameters = dict()
        if from_node_id is not None:
            headway_query_parameters["fromNodeId"] = from_node_id
        if to_node_id is not None:
            headway_query_parameters["toNodeId"] = to_node_id

        response_dict = self.__communication_layer.do_get_request(url_to_resource, headway_query_parameters)
        return converter_helpers.parse_to_timedelta(response_dict["headwayTime"])

    def get_headway_time(
        self,
        section_track_id: int,
        from_node_id: Optional[int],
        to_node_id: Optional[int],
        preceding_train_path_node_id: int,
        succeeding_train_path_node_id: int,
    ) -> datetime.timedelta:
        url_to_resource = "section-tracks/{0}/headway-times".format(section_track_id)
        headway_query_parameters = dict(
            precedingTrainPathNodeId=preceding_train_path_node_id,
            succeedingTrainPathNodeId=succeeding_train_path_node_id,
        )
        if from_node_id is not None:
            headway_query_parameters["fromNodeId"] = from_node_id
        if to_node_id is not None:
            headway_query_parameters["toNodeId"] = to_node_id

        response_dict = self.__communication_layer.do_get_request(url_to_resource, headway_query_parameters)
        return converter_helpers.parse_to_timedelta(response_dict["headwayTime"])

    def get_headway_time_for_train_path_nodes(
        self, preceding_train_path_node_id: int, succeeding_train_path_node_id: int
    ) -> datetime.timedelta:
        url_to_resource = "headway-times/between-train-path-nodes/{0}/{1}".format(
            preceding_train_path_node_id, succeeding_train_path_node_id
        )
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta(response_dict["separationTime"])

    def get_headway_time_for_train_path_nodes_on_section_track(
        self,
        preceding_train_path_node_id: int,
        succeeding_train_path_node_id: int,
        section_track_id: int,
        from_node_id: int,
        to_node_id: int,
    ) -> datetime.timedelta:
        url_to_resource = (
            "headway-times/between-train-path-nodes/{0}/{1}/for-section-track/{2}/in-direction/{3}/{4}".format(
                preceding_train_path_node_id,
                succeeding_train_path_node_id,
                section_track_id,
                from_node_id,
                to_node_id,
            )
        )
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta(response_dict["headwayTime"])

    def get_assignable_node_tracks_for_train_path_node(
        self, node_id: int, train_path_node_id: int, stop_status: Optional[StopStatus]
    ) -> List[AlgorithmNodeTrack]:
        url_to_resource = "nodes/{0}/node-tracks".format(node_id)
        if stop_status is not None:
            query_parameters = dict(assignableForTrainPathNodeId=train_path_node_id, stopStatus=stop_status.value)
        else:
            query_parameters = dict(assignableForTrainPathNodeId=train_path_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(AlgorithmNodeTrack, response_list)

    def get_assignable_station_tracks_on_train_path_node(self, train_path_node_id: int) -> List[AlgorithmNodeTrack]:
        url_to_resource = "assignable-station-tracks-on-train-path-node"
        query_parameters = dict(trainPathNodeId=train_path_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(AlgorithmNodeTrack, response_list)

    def update_node_track(
        self, train_id: int, train_path_node_id: int, station_track_id_or_none: Optional[int] = None
    ) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes/{1}:update-node-track".format(train_id, train_path_node_id)
        put_request_body = dict(nodeTrackId=to_json_converter.convert_any_object(station_track_id_or_none))
        response_dict = self.__communication_layer.do_put_request(url_to_resource, put_request_body)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def get_incoming_routing_edges(self, routing_point: RoutingPoint) -> List[IncomingNodeTrackRoutingEdge]:
        return _interface_helpers.do_get_routing_edges_request(
            self.__communication_layer,
            routing_point,
            converter_helpers.RoutingEdgeType.incoming_node_track,
        )

    def get_outgoing_routing_edges(self, routing_point: RoutingPoint) -> List[OutgoingNodeTrackRoutingEdge]:
        return _interface_helpers.do_get_routing_edges_request(
            self.__communication_layer, routing_point, converter_helpers.RoutingEdgeType.outgoing_node_track
        )

    def get_crossing_routing_edges(self, routing_point: RoutingPoint) -> List[CrossingRoutingEdge]:
        return _interface_helpers.do_get_routing_edges_request(
            self.__communication_layer, routing_point, converter_helpers.RoutingEdgeType.crossing
        )

    def get_routing_edges(self, routing_point: RoutingPoint) -> List[AnyRoutingEdgeIncomingOrCrossingOrOutgoing]:
        return _interface_helpers.do_get_routing_edges_request(self.__communication_layer, routing_point, None)

    def get_formation(self, formation_id: int) -> AlgorithmFormation:
        url_to_resource = "vehicles/formations/{0}".format(formation_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert(AlgorithmFormation, response_dict)

    def get_or_create_formation(self, vehicle_type_ids: List[int]) -> AlgorithmFormation:
        url_to_resource = "vehicles/formations"
        request_body = dict(vehicleTypeIDs=vehicle_type_ids)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body)
        return from_json_converter.convert(AlgorithmFormation, response_dict)

    def get_all_vehicle_types(self) -> List[AlgorithmVehicleType]:
        url_to_resource = "vehicles/types"
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_list(AlgorithmVehicleType, response_list)

    def get_vehicle_type(self, vehicle_type_id: int) -> AlgorithmVehicleType:
        url_to_resource = "vehicles/types/{0}".format(vehicle_type_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return self.__json_to_aidm_converter.process_json_to_aidm(response_dict, AlgorithmVehicleType)

    def get_links(
        self, time_window: TimeWindow
    ) -> List[Union[AlgorithmConnectionLink, AlgorithmAwaitArrivalLink, AlgorithmRosterLink]]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, None, None)

    def get_links_containing_any_node(
        self, time_window: TimeWindow, node_ids: List[int]
    ) -> List[Union[AlgorithmConnectionLink, AlgorithmAwaitArrivalLink, AlgorithmRosterLink]]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, None, node_ids)

    def get_connection_links(self, time_window: TimeWindow) -> List[AlgorithmConnectionLink]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, LinkType.connection, None)

    def get_connection_links_containing_any_node(
        self, time_window: TimeWindow, node_ids: List[int]
    ) -> List[AlgorithmConnectionLink]:
        return _interface_helpers.do_get_any_link(
            self.__communication_layer, time_window, LinkType.connection, node_ids
        )

    def get_await_arrival_links(self, time_window: TimeWindow) -> List[AlgorithmAwaitArrivalLink]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, LinkType.await_arrival, None)

    def get_await_arrival_links_containing_any_node(
        self, time_window: TimeWindow, node_ids: List[int]
    ) -> List[AlgorithmAwaitArrivalLink]:
        return _interface_helpers.do_get_any_link(
            self.__communication_layer, time_window, LinkType.await_arrival, node_ids
        )

    def get_roster_links(self, time_window: TimeWindow) -> List[AlgorithmRosterLink]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, LinkType.roster, None)

    def get_roster_links_containing_any_node(
        self, time_window: TimeWindow, node_ids: List[int]
    ) -> List[AlgorithmRosterLink]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, LinkType.roster, node_ids)

    def create_roster_links(self, roster_links: List[AlgorithmRosterLinkDefinition]) -> List[AlgorithmRosterLink]:
        url_to_resource = "links"
        request_body = to_json_converter.convert_any_object(roster_links)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body)
        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_link, response_dict)

    def delete_links(self, link_ids: List[int]):
        url_to_resource = "links"
        delete_request_body = dict(linkIDs=link_ids)
        self.__communication_layer.do_delete_request(url_to_resource, delete_request_body)

    def calculate_run_times(self, train_id: int) -> (UpdateTimesTrain, None):
        url_to_resource = "services/trains/{0}:run-time-calculation".format(train_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_json_to_update_train_times(response_dict)

    def notify_user(self, title: str, description: str) -> None:
        url_to_resource = "user-outputs/notifications"
        request_body = dict(title=title, description=description)
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def show_status_message(self, status_message: str, log_message: Optional[str] = None) -> None:
        url_to_resource = "user-outputs/status-messages"
        request_body = dict(statusMessage=status_message, logMessage=log_message)
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def create_table(self, table_definition: TableDefinition) -> int:
        url_to_resource = "user-outputs/tables"
        table_definition_as_json = to_json_converter.convert_any_object(table_definition)
        for column_index in range(len(table_definition_as_json["columns"])):
            table_definition_as_json["columns"][column_index]["header"] = table_definition_as_json["columns"][
                column_index
            ]["header"]["value"]
        response_dict = self.__communication_layer.do_post_request(url_to_resource, table_definition_as_json)
        return converter_helpers.convert_keys_to_snake_case(response_dict)["table_id"]

    def add_rows_to_table(self, table_id: int, table_rows: List[TableRow]):
        url_to_resource = "user-outputs/tables/{0}/rows".format(table_id)
        list_of_cells_per_row = to_json_converter.convert_any_object(table_rows)
        request_body = [dict(row=row["cells"]) for row in list_of_cells_per_row]
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def get_termination_request(self) -> TerminationRequest:
        url_to_resource = "user-inputs/signals"
        query_parameters = dict(signalType=SignalType.termination.value)
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_to_termination_request(response_dict)

    def get_bool_algorithm_parameter(self, key: str) -> bool:
        return _interface_helpers.do_get_any_parameter(self.__communication_layer, key)

    def get_int_algorithm_parameter(self, key: str) -> Maybe[int]:
        response_value: Optional[int] = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return Maybe(response_value)

    def get_enum_algorithm_parameter(
        self, enum_type: Type[from_json_converter.EnumType], key: str
    ) -> Maybe[from_json_converter.EnumType]:
        response_value = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return Maybe.create_from_json(
            response_value, from_json_converter.convert_algorithm_parameter_value_to_enum, enum_type
        )

    def get_floating_point_algorithm_parameter(self, key: str) -> Optional[FloatingPoint]:
        response_dict_or_none = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        if response_dict_or_none is None:
            return None
        else:
            return from_json_converter.convert(FloatingPoint, response_dict_or_none)

    def get_string_algorithm_parameter(self, key: str) -> str:
        response_string_or_none = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return "" if response_string_or_none is None else response_string_or_none

    def get_algorithm_train_parameter(self, key: str) -> AlgorithmTrain:
        response_dict = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return from_json_converter.convert_json_to_algorithm_train(response_dict)

    def get_algorithm_trains_parameter(self, key: str) -> List[AlgorithmTrain]:
        response_list = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return from_json_converter.convert_list(from_json_converter.convert_json_to_algorithm_train, response_list)

    def get_time_window_algorithm_parameter(self, key: str) -> Optional[TimeWindow]:
        response_dict_or_none = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        if response_dict_or_none is None:
            return None
        else:
            return from_json_converter.convert_json_to_time_window(response_dict_or_none)

    def get_node_track_closures(self, time_window: TimeWindow) -> List[AlgorithmNodeTrackClosure]:
        url_to_resource = "possessions/node-track-closures"
        query_parameters = to_json_converter.convert_any_object(time_window)
        response_list_of_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(
            from_json_converter.convert_json_to_algorithm_node_track_closure,
            response_list_of_dict
        )

    def get_section_track_closures(self, time_window: TimeWindow) -> List[AlgorithmSectionTrackClosure]:
        query_parameters = to_json_converter.convert_any_object(time_window)
        url_to_resource = "possessions/section-track-closures"
        response_list_of_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(
            from_json_converter.convert_json_to_algorithm_section_track_closure,
            response_list_of_dict
        )

    def get_section_running_time_penalties(self, time_window: TimeWindow)-> List[AlgorithmSectionRunningTimePenalty]:
        query_parameters = to_json_converter.convert_any_object(time_window)
        url_to_resource = "possessions/section-running-time-penalties"
        response_list_of_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return from_json_converter.convert_list(
            from_json_converter.convert_json_to_algorithm_section_running_time_penalty,
            response_list_of_dict
        )

    def get_movement_types(self) -> List[AlgorithmMovementType]:
        url_to_resource = "movement-types"
        response_list_of_dict = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_list(
            from_json_converter.convert_json_to_algorithm_movement_type,
            response_list_of_dict
        )

    def create_train_simulation(self, time_window: TimeWindow) -> None:
        query_parameters = to_json_converter.convert_any_object(time_window)
        url_to_resource = "services/trains/simulations"
        response = self.__communication_layer.do_put_request(url_to_resource, query_parameters)


    def get_train_simulation_trains(self) -> AlgorithmTrainSimulationTrain:
        url_to_resource = "services/trains/simulations/trains"
        response_list_of_dict = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_list(
            from_json_converter.convert_json_to_algorithm_train_simulation_train,
            response_list_of_dict
        )

    def get_next_train_simulation_event(self) -> AlgorithmTrainSimulationEvent:
        url_to_resource = "services/trains/simulations/events/next"
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert(
            from_json_converter.convert_json_to_algorithm_train_simulation_event,
            response_dict
        )

    def realize_next_train_simulation_event(self) -> AlgorithmTrainSimulationEvent:
        url_to_resource = "services/trains/simulations/events/next:realize"
        response_dict = self.__communication_layer.do_post_request(url_to_resource)
        return from_json_converter.convert(
            from_json_converter.convert_json_to_algorithm_train_simulation_event,
            response_dict
        )

    def calculate_running_time_penalties_on_train(self, train_id) -> List[RunningTimePenaltyOnTrainPath]:
        url_to_resource = "services/trains/{0}:calculate-running-time-penalties".format(train_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_list(
            from_json_converter.convert_json_to_running_time_penalties_on_train_path,
            response_list
        )

    def detect_conflicts(self, train_ids) -> List[AlgorithmConflict]:
        url_to_resource = "services/trains:detect-conflicts?trainIds={}".format(','.join([str(train_id) for train_id in train_ids]))
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return from_json_converter.convert_list(
            from_json_converter.convert_json_to_algorithm_conflict,
            response_list
        )
