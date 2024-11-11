from datetime import datetime, timedelta
from typing import Type, List, Optional, Union

from py_client.aidm.aidm_enum_classes import EnumType

import py_client.algorithm_interface._algorithm_interface_helpers as _interface_helpers
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
    FloatingPoint,
    AlgorithmRosterLinkDefinition,
    TableDefinition,
    AlgorithmNodeTrackClosure,
    AlgorithmSectionTrackClosure,
    AlgorithmSectionRunningTimePenalty,
    AlgorithmTrainSimulationTrain,
    AlgorithmMovementType,
    AlgorithmUnplannedStopPenalties,
    RunningTimePenaltyOnTrainPath,
    RunningTimeCalculationResult,
    ConflictDetectionArguments,
    AlgorithmTrainSimulationRealizationForecast,
    UserOutputSettings,
    ResetSummary,
    AlgorithmTrainSimulationCreationArguments,
)
from py_client.aidm.aidm_conflict import AlgorithmConflict
from py_client.aidm.aidm_link_classes import _AlgorithmLink
from py_client.aidm.aidm_routing_edge_classes import _RoutingEdge
from py_client.communication.communication_layer import CommunicationLayer
from py_client.conversion.json_to_aidm_converter import JsonToAidmConverter


class AlgorithmInterface:
    __communication_layer: CommunicationLayer

    def __init__(self, base_url: str):
        self.__communication_layer = CommunicationLayer(base_url)

    def __enter__(self):
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.__communication_layer.currentSession.close()

    @property
    def base_url(self) -> str:
        return self.__communication_layer.base_url

    def get_all_nodes(self) -> List[AlgorithmNode]:
        url_to_resource = "nodes"
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmNode])

    def get_node(self, node_id: int) -> AlgorithmNode:
        url_to_resource = "nodes/{0}".format(node_id)
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmNode)

    def get_preferred_routes_for_node(
        self,
        node_id: int,
        start_section_track_id: Optional[int],
        end_section_track_id: Optional[int],
    ) -> List[RoutingEdgePair]:
        url_to_resource = "nodes/{0}/preferred-routes".format(node_id)
        query_parameters = dict(startSectionTrackID=start_section_track_id, endSectionTrackID=end_section_track_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[RoutingEdgePair])

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
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[RoutingEdgePair])

    def get_preferred_starting_routes_for_node(self, node_id: int, end_section_track_id: Optional[int]) -> List[RoutingEdgePair]:
        url_to_resource = "nodes/{0}/preferred-routes".format(node_id)
        query_parameters = dict(endSectionTrackID=end_section_track_id, endInNode=False, startInNode=True)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[RoutingEdgePair])

    def get_preferred_ending_routes_for_node(self, node_id: int, start_section_track_id: Optional[int]) -> List[RoutingEdgePair]:
        url_to_resource = "nodes/{0}/preferred-routes".format(node_id)
        query_parameters = dict(startSectionTrackID=start_section_track_id, endInNode=True, startInNode=False)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[RoutingEdgePair])

    def get_all_section_tracks(self) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks"
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmSectionTrack])

    def get_section_track(self, section_track_id: int) -> AlgorithmSectionTrack:
        url_to_resource = "section-tracks/{0}".format(section_track_id)
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmSectionTrack)

    def get_nodes_with_section_track_from(self, from_node_id: int) -> List[AlgorithmNode]:
        url_to_resource = "nodes"
        query_parameters = dict(hasSectionTrackFromNodeId=from_node_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmNode])

    def get_nodes_with_section_track_to(self, to_node_id: int) -> List[AlgorithmNode]:
        url_to_resource = "nodes"
        query_parameters = dict(hasSectionTrackToNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmNode])

    def get_neighboring_nodes_between(self, from_node_id: int, to_node_id: int) -> List[AlgorithmNode]:
        url_to_resource = "nodes"
        query_parameters = dict(hasSectionTrackFromNodeId=from_node_id, hasSectionTrackToNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmNode])

    def get_section_tracks_from(self, from_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks"
        query_parameters = dict(fromNodeId=from_node_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmSectionTrack])

    def get_section_tracks_to(self, to_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks"
        query_parameters = dict(toNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmSectionTrack])

    def get_section_tracks_between(self, from_node_id: int, to_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks"
        query_parameters = dict(fromNodeId=from_node_id, toNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmSectionTrack])

    def get_parallel_section_tracks(self, section_track_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks"
        query_parameters = dict(parallelToSectionTrackId=section_track_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmSectionTrack])

    def get_directed_section_tracks(self, first_node_id: int, second_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = "section-tracks-between/{0}/{1}".format(first_node_id, second_node_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmSectionTrack])

    def get_neighbor_nodes(self, node_id: int) -> List[AlgorithmNode]:
        url_to_resource = "neighbor-nodes/{0}".format(node_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource)

        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmNode])

    def get_train_classification(self, train_id: int) -> AlgorithmTrainClassification:
        url_to_resource = "train-classifications/{0}".format(train_id)
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrainClassification)

    def get_train_classifications(self) -> List[AlgorithmTrainClassification]:
        url_to_resource = "train-classifications"
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmTrainClassification])

    def get_trains(self, time_window: TimeWindow) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        query_parameters = to_json_converter.convert_any_object(time_window)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmTrain])

    def get_trains_driving_any_node(self, time_window: TimeWindow, node_ids: List[int]) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        body = dict(filterNodeIds=node_ids)
        query_parameters = to_json_converter.convert_any_object(time_window)

        response_list = self.__communication_layer.do_get_request_with_body(url_to_resource, body=body, query_parameters=query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmTrain])

    def get_trains_cut_to_time_range(self, time_window: TimeWindow) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        cut_train_query_parameters = dict(cutTrain=True)
        query_parameters = _interface_helpers.merge_query_parameters([cut_train_query_parameters, to_json_converter.convert_any_object(time_window)])
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters=query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmTrain])

    def get_trains_cut_to_time_range_driving_any_node(self, time_window: TimeWindow, node_ids: List[int]) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        body = dict(filterNodeIds=node_ids)
        manual_converted_query_parameters = dict(cutTrain=True)
        query_parameters = _interface_helpers.merge_query_parameters([manual_converted_query_parameters, to_json_converter.convert_any_object(time_window)])
        response_list = self.__communication_layer.do_get_request_with_body(url_to_resource, body=body, query_parameters=query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmTrain])

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
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def cancel_train(self, train_id: int) -> None:
        url_to_resource = "trains/{0}:cancel".format(train_id)
        self.__communication_layer.do_delete_request(url_to_resource)

    def delete_train(self, train_id: int) -> None:
        url_to_resource = "trains/{0}:delete".format(train_id)
        self.__communication_layer.do_delete_request(url_to_resource)

    def update_movement_type(
        self, movement_type_id: Optional[int], train_id: int, from_train_path_node_id: int, to_train_path_node_id: Optional[int]
    ) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-movement-type".format(train_id)
        put_body_dict = dict(movementTypeId=movement_type_id, fromTrainPathNodeId=from_train_path_node_id, toTrainPathNodeId=to_train_path_node_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_dict)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def cancel_train_after(self, train_id: int, train_path_node_id: int) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes/{1}:cancel-after".format(train_id, train_path_node_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def cancel_train_before(self, train_id: int, train_path_node_id: int) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes/{1}:cancel-before".format(train_id, train_path_node_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def copy_train(self, train_id: int) -> AlgorithmTrain:
        url_to_resource = "trains/{0}:copy".format(train_id)
        response_dict = self.__communication_layer.do_post_request(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def copy_train_and_replace_route(self, train_id: int, node_ids: List[int]) -> AlgorithmTrain:
        url_to_resource = "trains/{0}:copy-and-replace-route".format(train_id)
        post_request_body = dict(routeViaNodeIds=node_ids)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, post_request_body)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def reroute_train(self, train_id: int, update_train_route: UpdateTrainRoute) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:reroute".format(train_id)
        put_request_body = to_json_converter.convert_any_object(update_train_route)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_request_body)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def update_section_track(self, train_id: int, train_path_node_id: int, section_track_id: int) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes/{1}:update-section-track".format(train_id, train_path_node_id)
        put_request_body = dict(sectionTrackId=section_track_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_request_body)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def update_train_times(self, train_id: int, update_times_train_path_nodes: List[UpdateTimesTrainPathNode]) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-times".format(train_id)
        put_body_list = to_json_converter.convert_any_object(update_times_train_path_nodes)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_list)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def update_train_trajectory_stop_times(self, train_id: int, update_stop_times_train_path_node: UpdateStopTimesTrainPathNode) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-trajectory-stop-times".format(train_id)
        put_body_list = to_json_converter.convert_any_object(update_stop_times_train_path_node)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_list)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def update_train_trajectory_run_times(
        self,
        train_id: int,
        update_run_times_train_path_segment: UpdateRunTimesTrainPathSegment,
    ) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-trajectory-run-times".format(train_id)
        put_body_dict = to_json_converter.convert_any_object(update_run_times_train_path_segment)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_dict)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def get_separation_time_in_junction_for_planned_train_paths(
        self,
        node_id: int,
        preceding_train_path_node_id: int,
        succeeding_train_path_node_id: int,
    ) -> Optional[timedelta]:
        url_to_resource = "nodes/{0}/separation-times".format(node_id)
        query_parameters = dict(
            precedingTrainPathNodeId=preceding_train_path_node_id,
            succeedingTrainPathNodeId=succeeding_train_path_node_id,
        )
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, Optional[timedelta])

    def get_separation_time_in_junction_for_routes(
        self,
        preceding_routing_edge: CrossingRoutingEdge,
        succeeding_routing_edge: CrossingRoutingEdge,
    ) -> Optional[timedelta]:
        url_to_resource = "nodes/{0}/separation-times".format(preceding_routing_edge.node_id)
        query_parameters = dict(
            precedingFromSectionTrackId=preceding_routing_edge.start_section_track_id,
            precedingToSectionTrackId=preceding_routing_edge.end_section_track_id,
            succeedingFromSectionTrackId=succeeding_routing_edge.start_section_track_id,
            succeedingToSectionTrackId=succeeding_routing_edge.end_section_track_id,
        )

        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, Optional[timedelta])

    def get_separation_time_in_station_for_node_track_reoccupation(self, node_id: int, node_track_id: int) -> timedelta:
        url_to_resource = "nodes/{0}/separation-times".format(node_id)
        query_parameters = dict(nodeTrackId=node_track_id)
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, timedelta)

    def get_separation_time_in_station_for_planned_train_paths(
        self,
        node_id: int,
        preceding_train_path_node_id: int,
        preceding_train_stop_status: Optional[StopStatus],
        preceding_station_entry_or_exit: StationEntryOrExit,
        succeeding_train_path_node_id: int,
        succeeding_train_stop_status: Optional[StopStatus],
        succeeding_station_entry_or_exit: StationEntryOrExit,
    ) -> Optional[timedelta]:
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

        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, Optional[timedelta])

    def get_separation_time_in_station_for_routes(
        self,
        preceding_train_routing_edge: _RoutingEdge,
        preceding_train_stop_status: StopStatus,
        succeeding_train_routing_edge: _RoutingEdge,
        succeeding_train_stop_status: StopStatus,
    ) -> Optional[timedelta]:
        url_to_resource = "nodes/{0}/separation-times".format(preceding_train_routing_edge.node_id)
        query_parameters = _interface_helpers.create_query_parameters_from_preceding_and_succeeding_routing_edge(
            preceding_train_routing_edge, succeeding_train_routing_edge
        )
        query_parameters["precedingStopStatus"] = preceding_train_stop_status.value
        query_parameters["succeedingStopStatus"] = succeeding_train_stop_status.value

        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)

        return JsonToAidmConverter().process_json_to_aidm(response_dict, Optional[timedelta])

    def get_default_headway_time(self, section_track_id: int, from_node_id: Optional[int], to_node_id: Optional[int]) -> timedelta:
        url_to_resource = "section-tracks/{0}/headway-times".format(section_track_id)
        headway_query_parameters = dict()
        if from_node_id is not None:
            headway_query_parameters["fromNodeId"] = from_node_id
        if to_node_id is not None:
            headway_query_parameters["toNodeId"] = to_node_id

        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, headway_query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, timedelta)

    def get_headway_time(
        self,
        section_track_id: int,
        from_node_id: Optional[int],
        to_node_id: Optional[int],
        preceding_train_path_node_id: int,
        succeeding_train_path_node_id: int,
    ) -> timedelta:
        url_to_resource = "section-tracks/{0}/headway-times".format(section_track_id)
        headway_query_parameters = dict(
            precedingTrainPathNodeId=preceding_train_path_node_id,
            succeedingTrainPathNodeId=succeeding_train_path_node_id,
        )
        if from_node_id is not None:
            headway_query_parameters["fromNodeId"] = from_node_id
        if to_node_id is not None:
            headway_query_parameters["toNodeId"] = to_node_id

        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, headway_query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, timedelta)

    def get_headway_time_for_train_path_nodes(self, preceding_train_path_node_id: int, succeeding_train_path_node_id: int) -> timedelta:
        url_to_resource = "headway-times/between-train-path-nodes/{0}/{1}".format(preceding_train_path_node_id, succeeding_train_path_node_id)
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, timedelta)

    def get_headway_time_for_train_path_nodes_on_section_track(
        self,
        preceding_train_path_node_id: int,
        succeeding_train_path_node_id: int,
        section_track_id: int,
        from_node_id: int,
        to_node_id: int,
    ) -> timedelta:
        url_to_resource = "headway-times/between-train-path-nodes/{0}/{1}/for-section-track/{2}/in-direction/{3}/{4}".format(
            preceding_train_path_node_id,
            succeeding_train_path_node_id,
            section_track_id,
            from_node_id,
            to_node_id,
        )
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, timedelta)

    def get_assignable_node_tracks_for_train_path_node(
        self, node_id: int, train_path_node_id: int, stop_status: Optional[StopStatus]
    ) -> List[AlgorithmNodeTrack]:
        url_to_resource = "nodes/{0}/node-tracks".format(node_id)
        if stop_status is not None:
            query_parameters = dict(assignableForTrainPathNodeId=train_path_node_id, stopStatus=stop_status.value)
        else:
            query_parameters = dict(assignableForTrainPathNodeId=train_path_node_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmNodeTrack])

    def get_assignable_station_tracks_on_train_path_node(self, train_path_node_id: int) -> List[AlgorithmNodeTrack]:
        url_to_resource = "assignable-station-tracks-on-train-path-node"
        query_parameters = dict(trainPathNodeId=train_path_node_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmNodeTrack])

    def update_node_track(self, train_id: int, train_path_node_id: int, node_track_id: Optional[int] = None) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes/{1}:update-node-track".format(train_id, train_path_node_id)
        put_request_body = dict(nodeTrackId=to_json_converter.convert_any_object(node_track_id))
        response_dict = self.__communication_layer.do_put_request(url_to_resource, put_request_body)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def get_incoming_routing_edges(self, routing_point: RoutingPoint) -> List[IncomingNodeTrackRoutingEdge]:
        return _interface_helpers.do_get_routing_edges_request(
            self.__communication_layer,
            routing_point,
            converter_helpers.RoutingEdgeType.incoming_node_track,
        )

    def get_outgoing_routing_edges(self, routing_point: RoutingPoint) -> List[OutgoingNodeTrackRoutingEdge]:
        return _interface_helpers.do_get_routing_edges_request(self.__communication_layer, routing_point, converter_helpers.RoutingEdgeType.outgoing_node_track)

    def get_crossing_routing_edges(self, routing_point: RoutingPoint) -> List[CrossingRoutingEdge]:
        return _interface_helpers.do_get_routing_edges_request(self.__communication_layer, routing_point, converter_helpers.RoutingEdgeType.crossing)

    def get_routing_edges(self, routing_point: RoutingPoint) -> List[AnyRoutingEdgeIncomingOrCrossingOrOutgoing]:
        return _interface_helpers.do_get_routing_edges_request(self.__communication_layer, routing_point, None)

    def get_formation(self, formation_id: int) -> AlgorithmFormation:
        url_to_resource = "vehicles/formations/{0}".format(formation_id)
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmFormation)

    def get_or_create_formation(self, vehicle_type_ids: List[int]) -> AlgorithmFormation:
        url_to_resource = "vehicles/formations"
        request_body = dict(vehicleTypeIDs=vehicle_type_ids)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmFormation)

    def get_all_vehicle_types(self) -> List[AlgorithmVehicleType]:
        url_to_resource = "vehicles/types"
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmVehicleType])

    def get_vehicle_type(self, vehicle_type_id: int) -> AlgorithmVehicleType:
        url_to_resource = "vehicles/types/{0}".format(vehicle_type_id)
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmVehicleType)

    def get_links(self, time_window: TimeWindow) -> List[Union[AlgorithmConnectionLink, AlgorithmAwaitArrivalLink, AlgorithmRosterLink]]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, None, None)

    def get_links_containing_any_node(
        self, time_window: TimeWindow, node_ids: List[int]
    ) -> List[Union[AlgorithmConnectionLink, AlgorithmAwaitArrivalLink, AlgorithmRosterLink]]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, None, node_ids)

    def get_connection_links(self, time_window: TimeWindow) -> List[AlgorithmConnectionLink]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, LinkType.connection, None)

    def get_connection_links_containing_any_node(self, time_window: TimeWindow, node_ids: List[int]) -> List[AlgorithmConnectionLink]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, LinkType.connection, node_ids)

    def get_await_arrival_links(self, time_window: TimeWindow) -> List[AlgorithmAwaitArrivalLink]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, LinkType.await_arrival, None)

    def get_await_arrival_links_containing_any_node(self, time_window: TimeWindow, node_ids: List[int]) -> List[AlgorithmAwaitArrivalLink]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, LinkType.await_arrival, node_ids)

    def get_roster_links(self, time_window: TimeWindow) -> List[AlgorithmRosterLink]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, LinkType.roster, None)

    def get_roster_links_containing_any_node(self, time_window: TimeWindow, node_ids: List[int]) -> List[AlgorithmRosterLink]:
        return _interface_helpers.do_get_any_link(self.__communication_layer, time_window, LinkType.roster, node_ids)

    def create_roster_links(self, roster_links: List[AlgorithmRosterLinkDefinition]) -> List[AlgorithmRosterLink]:
        url_to_resource = "links"
        request_body = to_json_converter.convert_any_object(roster_links)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, List[_AlgorithmLink])

    def delete_links(self, link_ids: List[int]):
        url_to_resource = "links"
        delete_request_body = dict(linkIDs=link_ids)
        self.__communication_layer.do_delete_request(url_to_resource, delete_request_body)

    def calculate_running_times(self, train_id: int) -> RunningTimeCalculationResult:
        url_to_resource = "services/trains/{0}:calculate-running-times".format(train_id)
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, RunningTimeCalculationResult)

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
            table_definition_as_json["columns"][column_index]["header"] = table_definition_as_json["columns"][column_index]["header"]["value"]
        response_dict = self.__communication_layer.do_post_request(url_to_resource, table_definition_as_json)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, int)

    def add_rows_to_table(self, table_id: int, table_rows: List[TableRow]):
        url_to_resource = "user-outputs/tables/{0}/rows".format(table_id)
        list_of_cells_per_row = to_json_converter.convert_any_object(table_rows)
        request_body = [dict(row=row["cells"]) for row in list_of_cells_per_row]
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def get_termination_request(self) -> TerminationRequest:
        url_to_resource = "user-inputs/signals"
        query_parameters = dict(signalType=SignalType.termination.value)
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, TerminationRequest)

    def get_bool_algorithm_parameter(self, key: str) -> bool:
        return _interface_helpers.do_get_any_parameter(self.__communication_layer, key)

    def get_bool_list_algorithm_parameter(self, key: str) -> bool:
        response_value: Optional[int] = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_value, List[bool])

    def get_int_algorithm_parameter(self, key: str) -> Optional[int]:
        response_value: Optional[int] = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_value, Optional[int])

    def get_enum_algorithm_parameter(self, enum_type: Type[EnumType], key: str) -> Optional[EnumType]:
        response_value = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_value, Optional[enum_type])

    def get_floating_point_algorithm_parameter(self, key: str) -> FloatingPoint:
        response_dict_or_none = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_dict_or_none, FloatingPoint)

    def get_floating_point_list_algorithm_parameter(self, key: str) -> List[FloatingPoint]:
        response_dict_or_none = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_dict_or_none, List[FloatingPoint])

    def get_string_algorithm_parameter(self, key: str) -> Optional[str]:
        response_string_or_none = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_string_or_none, Optional[str])

    def get_string_list_algorithm_parameter(self, key: str) -> List[str]:
        response_string_or_none = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_string_or_none, List[str])

    def get_algorithm_node_parameter(self, key: str) -> AlgorithmNode:
        response_dict = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmNode)

    def get_algorithm_nodes_parameter(self, key: str) -> List[AlgorithmNode]:
        response_dict = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, List[AlgorithmNode])

    def get_algorithm_train_parameter(self, key: str) -> AlgorithmTrain:
        response_dict = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrain)

    def get_algorithm_trains_parameter(self, key: str) -> List[AlgorithmTrain]:
        response_list = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmTrain])

    def get_time_window_algorithm_parameter(self, key: str) -> TimeWindow:
        response_dict_or_none = _interface_helpers.do_get_any_parameter(self.__communication_layer, key)
        return JsonToAidmConverter().process_json_to_aidm(response_dict_or_none, TimeWindow)

    def get_node_track_closures(self, time_window: TimeWindow) -> List[AlgorithmNodeTrackClosure]:
        url_to_resource = "possessions/node-track-closures"
        query_parameters = to_json_converter.convert_any_object(time_window)
        response_list_of_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list_of_dict, List[AlgorithmNodeTrackClosure])

    def get_section_track_closures(self, time_window: TimeWindow) -> List[AlgorithmSectionTrackClosure]:
        query_parameters = to_json_converter.convert_any_object(time_window)
        url_to_resource = "possessions/section-track-closures"
        response_list_of_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list_of_dict, List[AlgorithmSectionTrackClosure])

    def get_section_running_time_penalties(self, time_window: TimeWindow) -> List[AlgorithmSectionRunningTimePenalty]:
        query_parameters = to_json_converter.convert_any_object(time_window)
        url_to_resource = "possessions/section-running-time-penalties"
        response_list_of_dict = self.__communication_layer.do_get_request_without_body(url_to_resource, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list_of_dict, List[AlgorithmSectionRunningTimePenalty])

    def get_movement_types(self) -> List[AlgorithmMovementType]:
        url_to_resource = "movement-types"
        response_list_of_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_list_of_dict, List[AlgorithmMovementType])

    def create_train_simulation(self, algorithm_train_simulation_creation_arguments: AlgorithmTrainSimulationCreationArguments) -> None:
        url_to_resource = "services/trains/simulations"
        self.__communication_layer.do_put_request(url_to_resource, to_json_converter.convert_any_object(algorithm_train_simulation_creation_arguments))

    def reset_trains(self) -> ResetSummary:
        url_to_resource = "services/trains:reset"
        response_dict = self.__communication_layer.do_delete_request(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, ResetSummary)

    def get_train_simulation_trains(self) -> List[AlgorithmTrainSimulationTrain]:
        url_to_resource = "services/trains/simulations/trains"
        response_list_of_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_list_of_dict, List[AlgorithmTrainSimulationTrain])

    def get_next_train_simulation_event(self) -> AlgorithmTrainSimulationRealizationForecast:
        url_to_resource = "services/trains/simulations/events/next"
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrainSimulationRealizationForecast)

    def realize_next_train_simulation_event(self) -> AlgorithmTrainSimulationRealizationForecast:
        url_to_resource = "services/trains/simulations/events/next:realize"
        response_dict = self.__communication_layer.do_post_request(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrainSimulationRealizationForecast)

    def calculate_running_time_penalties_on_train(self, train_id: int) -> List[RunningTimePenaltyOnTrainPath]:
        url_to_resource = "services/trains/{0}:calculate-running-time-penalties".format(train_id)
        response_list = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[RunningTimePenaltyOnTrainPath])

    def detect_conflicts(self, arguments: ConflictDetectionArguments) -> List[AlgorithmConflict]:
        url_to_resource = "services/trains:detect-conflicts"

        query_parameters = dict()
        if arguments.filter_train_id is not None:
            query_parameters["trainId"] = arguments.filter_train_id

        if arguments.time_window is not None:
            query_parameters = _interface_helpers.merge_query_parameters([query_parameters, to_json_converter.convert_any_object(arguments.time_window)])

        body = self.__construct_body(arguments)
        response_list = self.__communication_layer.do_get_request_with_body(url_to_resource, body, query_parameters)
        return JsonToAidmConverter().process_json_to_aidm(response_list, List[AlgorithmConflict])

    def __construct_body(self, arguments: ConflictDetectionArguments):
        location = dict(nodeIds=arguments.filter_node_ids, sectionTrackIds=arguments.filter_section_track_ids)
        filters = dict(location=location, conflictTypes=to_json_converter.convert_any_object(arguments.filter_conflict_types))
        body = dict(trainIds=arguments.train_ids, filters=filters)
        return body

    def has_changed_links(self) -> bool:
        url_to_resource = "links:has-changed"
        response = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response, bool)

    def has_changed_trains(self) -> bool:
        url_to_resource = "trains:has-changed"
        response = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response, bool)

    def postpone_next_train_simulation_event(self, additional_delay: timedelta) -> AlgorithmTrainSimulationRealizationForecast:
        url_to_resource = "services/trains/simulations/events/next:postpone"
        converted_additional_delay = to_json_converter.convert_any_object(additional_delay)
        post_request_body = dict(additionalDelay=converted_additional_delay)
        response = self.__communication_layer.do_post_request(url_to_resource, post_request_body)
        return JsonToAidmConverter().process_json_to_aidm(response, AlgorithmTrainSimulationRealizationForecast)

    def replace_next_train_simulation_event_by_stop(self) -> AlgorithmTrainSimulationRealizationForecast:
        url_to_resource = "services/trains/simulations/events/next:replace-by-stop"
        response = self.__communication_layer.do_post_request(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response, AlgorithmTrainSimulationRealizationForecast)

    def calculate_maximum_headway_time(self) -> timedelta:
        url_to_resource = "section-tracks/headway-times:calculate-maximum"
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, timedelta)

    def calculate_maximum_separation_time(self, node_id: int = None) -> timedelta:
        # Overloaded method is not possible in python, need to branch on arguments
        if node_id is None:
            url_to_resource = "nodes/separation-times:calculate-maximum"
            response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
            return JsonToAidmConverter().process_json_to_aidm(response_dict, timedelta)
        else:
            url_to_resource = "nodes/{}/separation-times:calculate-maximum".format(node_id)
            response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
            return JsonToAidmConverter().process_json_to_aidm(response_dict, timedelta)

    def get_unplanned_stop_penalties(self, train_id: int) -> AlgorithmUnplannedStopPenalties:
        url_to_resource = "trains/{}/unplanned-stop-penalties".format(train_id)
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmUnplannedStopPenalties)

    def get_user_output_settings(self) -> UserOutputSettings:
        url_to_resource = "user-outputs/settings"
        response_dict = self.__communication_layer.do_get_request_without_body(url_to_resource)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, UserOutputSettings)

    def persist_trains(self, scenario_description: str) -> str:
        url_to_resource = "services/trains:persist"
        request_body = dict(description=scenario_description)
        response_dict = self.__communication_layer.do_post_request(url_to_resource, request_body)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, str)

    def update_node_track_of_next_event(self, node_track_id: int) -> AlgorithmTrainSimulationRealizationForecast:
        url_to_resource = "services/trains/simulations/events/next:update-node-track"
        put_request_body = dict(nodeTrackId=node_track_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_request_body)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrainSimulationRealizationForecast)

    def update_node_track_of_future_event(self, event_id: int, node_track_id: int) -> AlgorithmTrainSimulationRealizationForecast:
        url_to_resource = "services/trains/simulations/events/{0}:update-node-track".format(event_id)
        put_request_body = dict(nodeTrackId=node_track_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_request_body)
        return JsonToAidmConverter().process_json_to_aidm(response_dict, AlgorithmTrainSimulationRealizationForecast)
