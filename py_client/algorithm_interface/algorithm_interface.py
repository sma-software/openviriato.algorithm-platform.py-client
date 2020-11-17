from typing import Union

from multipledispatch import dispatch

from py_client.aidm import *
from py_client.algorithm_interface.algorithm_interface_helpers import merge_query_parameters, \
    create_query_parameters_from_preceding_and_succeeding_routing_edge
from py_client.communication import communication_layer
from py_client.conversion import object_to_algorithm_platform_json_converter, converter_helpers, \
    algorithm_platform_json_to_aidm_converter


class AlgorithmInterface:
    __communication_layer: communication_layer.CommunicationLayer

    def __init__(self, base_url: str):
        self.__communication_layer = communication_layer.CommunicationLayer(base_url)

    def __enter__(self):
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.__communication_layer.currentSession.close()

    @property
    def base_url(self) -> str:
        return self.__communication_layer.base_url

    def get_all_nodes(self) -> List[AlgorithmNode]:
        url_to_resource = 'nodes'
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_node,
            response_list)

    def get_node(self, node_id: int) -> AlgorithmNode:
        url_to_resource = 'nodes/{0}'.format(node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_node(response_dict)

    def get_all_section_tracks(self) -> List[AlgorithmSectionTrack]:
        url_to_resource = 'section-tracks'
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_section_track(self, section_track_id: int) -> AlgorithmSectionTrack:
        url_to_resource = 'section-tracks/{0}'.format(section_track_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert(AlgorithmSectionTrack, response_dict)

    def get_nodes_with_section_track_from(self, from_node_id: int) -> List[AlgorithmNode]:
        url_to_resource = 'nodes'
        request_parameters = dict(hasSectionTrackFromNodeId=from_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_node,
            response_list)

    def get_nodes_with_section_track_to(self, to_node_id: int) -> List[AlgorithmNode]:
        url_to_resource = 'nodes'
        request_parameters = dict(hasSectionTrackToNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_node,
            response_list)

    def get_neighboring_nodes_between(self, from_node_id: int, to_node_id: int) -> List[AlgorithmNode]:
        url_to_resource = 'nodes'
        request_parameters = dict(hasSectionTrackFromNodeId=from_node_id, hasSectionTrackToNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_node,
            response_list
        )

    def get_section_tracks_from(self, from_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = 'section-tracks'
        request_parameters = dict(fromNodeId=from_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_section_tracks_to(self, to_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = 'section-tracks'
        request_parameters = dict(toNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_section_tracks_between(self, from_node_id: int, to_node_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = 'section-tracks'
        request_parameters = dict(fromNodeId=from_node_id, toNodeId=to_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_parallel_section_tracks(self, section_track_id: int) -> List[AlgorithmSectionTrack]:
        url_to_resource = 'section-tracks'
        request_parameters = dict(parallelToSectionTrackId=section_track_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, request_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_directed_section_tracks(
            self,
            first_node_id: int,
            second_node_id: int
    ) -> List[AlgorithmSectionTrack]:
        url_to_resource = 'section-tracks-between/{0}/{1}'.format(first_node_id, second_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert_list(AlgorithmSectionTrack, response_list)

    def get_neighbor_nodes(self, node_id: int) -> List[AlgorithmNode]:
        url_to_resource = 'neighbor-nodes/{0}'.format(node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource)

        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_node,
            response_list
        )

    def get_train_classification(self, train_id: int) -> AlgorithmTrainClassification:
        url_to_resource = 'train-classifications/{0}'.format(train_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert(AlgorithmTrainClassification,
                                                                 response_dict)

    def get_train_classifications(self) -> List[AlgorithmTrainClassification]:
        url_to_resource = 'train-classifications'
        response_list = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert_list(AlgorithmTrainClassification,
                                                                      response_list)

    def get_trains(self, time_window: TimeWindow) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        query_parameters = object_to_algorithm_platform_json_converter.convert_any_object(time_window)
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters)

        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train,
            response_list
        )

    def get_trains_driving_any_node(
            self,
            time_window: TimeWindow,
            node_ids: List[int]
    ) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        manual_converted_query_parameters = dict(nodeFilter=node_ids)
        query_parameters = merge_query_parameters(
            [
                manual_converted_query_parameters,
                object_to_algorithm_platform_json_converter.convert_any_object(time_window)
            ]
        )
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters=query_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train,
            response_list
        )

    def get_trains_cut_to_time_range(self, time_window: TimeWindow) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        cut_train_query_parameters = dict(cutTrain=True)
        query_parameters = merge_query_parameters(
            [
                cut_train_query_parameters,
                object_to_algorithm_platform_json_converter.convert_any_object(time_window)
            ]
        )
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters=query_parameters)

        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train,
            response_list
        )

    def get_trains_cut_to_time_range_driving_any_node(
            self,
            time_window: TimeWindow,
            node_ids: List[int]
    ) -> List[AlgorithmTrain]:
        url_to_resource = "trains"
        manual_converted_query_parameters = dict(cutTrain=True, nodeFilter=node_ids)
        query_parameters = merge_query_parameters(
            [
                manual_converted_query_parameters,
                object_to_algorithm_platform_json_converter.convert_any_object(time_window)
            ]
        )
        response_list = self.__communication_layer.do_get_request(url_to_resource, query_parameters=query_parameters)

        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train,
            response_list
        )

    def cancel_train(self, train_id: int) -> int:
        url_to_resource = 'trains/{0}'.format(train_id)
        return self.__communication_layer.do_delete_request(url_to_resource)

    def cancel_train_after(self, train_id: int, train_path_node_id: int) -> AlgorithmTrain:
        url_to_resource = 'trains/{0}/train-path-nodes/{1}:cancel-after'.format(train_id, train_path_node_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train(response_dict)

    def cancel_train_before(self, train_id: int, train_path_node_id: int) -> AlgorithmTrain:
        url_to_resource = 'trains/{0}/train-path-nodes/{1}:cancel-before'.format(train_id, train_path_node_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train(response_dict)

    def clone_train(self, train_id: int) -> AlgorithmTrain:
        url_to_resource = 'trains/{0}:clone'.format(train_id)
        response_dict = self.__communication_layer.do_post_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train(response_dict)

    def reroute_train(self, train_id: int, route: UpdateTrainRoute):
        url_to_resource = "trains/{0}/train-path-nodes:reroute".format(train_id)
        put_request_body = object_to_algorithm_platform_json_converter.convert_any_object(route)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_request_body)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train(response_dict)

    def update_section_track(self, train_id: int, train_path_node_id: int, section_track_id: int) -> AlgorithmTrain:
        url_to_resource = 'trains/{0}/train-path-nodes/{1}:update-section-track'.format(train_id, train_path_node_id)
        put_request_body = dict(sectionTrackId=section_track_id)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_request_body)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train(response_dict)

    def update_train_times(
            self,
            train_id: int,
            update_train_times_nodes: List[UpdateTimesTrainPathNode]
    ) -> AlgorithmTrain:
        url_to_resource = 'trains/{0}/train-path-nodes:update-times'.format(train_id)
        put_body_list = object_to_algorithm_platform_json_converter.convert_any_object(update_train_times_nodes)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_list)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train(response_dict)

    @dispatch(object, UpdateStopTimesTrainPathNode)
    def update_trajectory(
            self,
            train_id: int,
            update_train_stop_times_node: UpdateStopTimesTrainPathNode
    ) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-trajectory-stop-times".format(train_id)
        put_body_list = object_to_algorithm_platform_json_converter.convert_any_object(update_train_stop_times_node)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_list)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train(response_dict)

    @dispatch(object, UpdateRunTimesTrainPathSegment)
    def update_trajectory(
            self,
            train_id: int,
            update_run_times_train_path_segment: UpdateRunTimesTrainPathSegment
    ) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes:update-trajectory-run-times".format(train_id)
        put_body_dict = object_to_algorithm_platform_json_converter.convert_any_object(
            update_run_times_train_path_segment)
        response_dict = self.__communication_layer.do_put_request(url_to_resource, request_body=put_body_dict)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train(response_dict)

    def get_separation_time_in_junction_for_planned_train_paths(
            self,
            node_id: int,
            preceding_train_path_node_id: int,
            succeeding_train_path_node_id: int
    ) -> Optional[datetime.timedelta]:
        url_to_resource = 'nodes/{0}/separation-times'.format(node_id)
        query_parameters = dict(
            precedingTrainPathNodeId=preceding_train_path_node_id,
            succeedingTrainPathNodeId=succeeding_train_path_node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta_or_none(response_dict["separationTime"])

    def get_separation_time_in_junction_for_routes(
            self,
            preceding_routing_edge: CrossingRoutingEdge,
            succeeding_routing_edge: CrossingRoutingEdge
    ) -> Optional[datetime.timedelta]:
        url_to_resource = 'nodes/{0}/separation-times'.format(preceding_routing_edge.node_id)
        query_parameters = dict(
            precedingFromSectionTrackId=preceding_routing_edge.start_section_track_id,
            precedingToSectionTrackId=preceding_routing_edge.end_section_track_id,
            succeedingFromSectionTrackId=succeeding_routing_edge.start_section_track_id,
            succeedingToSectionTrackId=succeeding_routing_edge.end_section_track_id)

        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta_or_none(response_dict["separationTime"])

    def get_separation_time_in_station_for_node_track_reoccupation(
            self,
            node_id: int,
            node_track_id: int) -> datetime.timedelta:
        url_to_resource = 'nodes/{0}/separation-times'.format(node_id)
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
            succeeding_station_entry_or_exit: StationEntryOrExit
    ) -> Optional[datetime.timedelta]:

        url_to_resource = "nodes/{0}/separation-times".format(node_id)

        preceding_entry_or_exit = object_to_algorithm_platform_json_converter.convert_any_object(
            preceding_station_entry_or_exit)
        succeeding_entry_or_exit = object_to_algorithm_platform_json_converter.convert_any_object(
            succeeding_station_entry_or_exit)

        query_parameters = dict(
            precedingTrainPathNodeId=preceding_train_path_node_id,
            precedingEntryOrExit=preceding_entry_or_exit,
            succeedingTrainPathNodeId=succeeding_train_path_node_id,
            succeedingEntryOrExit=succeeding_entry_or_exit)

        if preceding_train_stop_status is not None:
            query_parameters['precedingStopStatus'] = object_to_algorithm_platform_json_converter \
                .convert_any_object(preceding_train_stop_status)
        if succeeding_train_stop_status is not None:
            query_parameters['succeedingStopStatus'] = object_to_algorithm_platform_json_converter \
                .convert_any_object(succeeding_train_stop_status)

        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return converter_helpers.parse_to_timedelta_or_none(response_dict['separationTime'])

    def get_separation_time_in_station_for_routes(
            self,
            preceding_train_routing_edge: Union[IncomingRoutingEdge, OutgoingRoutingEdge],
            preceding_stop_status: StopStatus,
            succeeding_train_routing_edge: Union[IncomingRoutingEdge, OutgoingRoutingEdge],
            succeeding_stop_status: StopStatus
    ) -> Optional[datetime.timedelta]:

        url_to_resource = 'nodes/{0}/separation-times'.format(preceding_train_routing_edge.node_id)
        query_parameters = create_query_parameters_from_preceding_and_succeeding_routing_edge(
            preceding_train_routing_edge,
            succeeding_train_routing_edge)
        query_parameters['precedingStopStatus'] = object_to_algorithm_platform_json_converter \
            .convert_any_object(preceding_stop_status)
        query_parameters['succeedingStopStatus'] = object_to_algorithm_platform_json_converter \
            .convert_any_object(succeeding_stop_status)

        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)

        return converter_helpers.parse_to_timedelta_or_none(response_dict["separationTime"])

    def get_default_headway_time(
            self,
            section_track_id: int,
            from_node_id: Optional[int],
            to_node_id: Optional[int]
    ) -> datetime.timedelta:

        url_to_resource = "section-tracks/{0}/headway-times".format(section_track_id)
        headway_query_parameters = dict()
        if from_node_id is not None:
            headway_query_parameters['fromNodeId'] = from_node_id
        if to_node_id is not None:
            headway_query_parameters['toNodeId'] = to_node_id

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
            precedingTrainPathNodeId=preceding_train_path_node_id,
            succeedingTrainPathNodeId=succeeding_train_path_node_id)
        if from_node_id is not None:
            headway_query_parameters['fromNodeId'] = from_node_id
        if to_node_id is not None:
            headway_query_parameters['toNodeId'] = to_node_id

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
        url_to_resource = 'headway-times/between-train-path-nodes/{0}/{1}/for-section-track/{2}/in-direction/{3}/{4}' \
            .format(preceding_train_path_node_id,
                    succeeding_train_path_node_id,
                    section_track_id,
                    from_node_id,
                    to_node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return converter_helpers.parse_to_timedelta(response_dict["headwayTime"])

    def get_assignable_node_tracks_for_train_path_node(
            self,
            node_id: int,
            train_path_node_id: int,
            stop_status: Optional[StopStatus]
    ) -> List[AlgorithmNodeTrack]:
        url_to_resource = "nodes/{0}/node-tracks".format(node_id)
        if stop_status is not None:
            stop_status_value = object_to_algorithm_platform_json_converter.convert_any_object(stop_status)
            get_request_params = dict(assignableForTrainPathNodeId=train_path_node_id, stopStatus=stop_status_value)
        else:
            get_request_params = dict(assignableForTrainPathNodeId=train_path_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_aidm_converter.convert_list(AlgorithmNodeTrack, response_list)

    def get_assignable_station_tracks_on_train_path_node(
            self,
            train_path_node_id: int
    ) -> List[AlgorithmNodeTrack]:
        url_to_resource = "assignable-station-tracks-on-train-path-node"
        get_request_params = dict(trainPathNodeId=train_path_node_id)
        response_list = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_aidm_converter.convert_list(AlgorithmNodeTrack, response_list)

    def update_node_track(
            self,
            train_id: int,
            train_path_node_id: int,
            station_track_id_or_none: Optional[int] = None
    ) -> AlgorithmTrain:
        url_to_resource = "trains/{0}/train-path-nodes/{1}:update-node-track".format(train_id, train_path_node_id)
        put_request_body = dict(
            nodeTrackId=object_to_algorithm_platform_json_converter.convert_any_object(station_track_id_or_none))
        response_dict = self.__communication_layer.do_put_request(url_to_resource, put_request_body)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train(response_dict)

    def get_incoming_routing_edges(self, routing_point: RoutingPoint) -> IncomingRoutingEdgeSet:
        url_to_resource = "nodes/{0}/incoming-routing-edges".format(routing_point.node_id)
        if routing_point.node_track_id is not None:
            get_request_params = dict(endNodeTrackId=routing_point.node_track_id)
        else:
            get_request_params = dict()
        response_dict = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_incoming_routing_edge_set(response_dict)

    def get_outgoing_routing_edges(self, routing_point: RoutingPoint) -> OutgoingRoutingEdgeSet:
        url_to_resource = "nodes/{0}/outgoing-routing-edges".format(routing_point.node_id)
        if routing_point.node_track_id is not None:
            get_request_params = dict(startNodeTrackId=routing_point.node_track_id)
        else:
            get_request_params = dict()
        response_dict = self.__communication_layer.do_get_request(url_to_resource, get_request_params)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_outgoing_routing_edge_set(response_dict)

    def get_crossing_routing_edges(self, routing_point: RoutingPoint) -> CrossingRoutingEdgeSet:
        url_to_resource = "nodes/{0}/crossing-routing-edges".format(routing_point.node_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_crossing_routing_edge_set(response_dict)

    def get_formation(self, formation_id: int) -> AlgorithmFormation:
        url_to_resource = "vehicles/formations/{0}".format(formation_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert(AlgorithmFormation, response_dict)

    def get_vehicle_type(self, vehicle_type_id: int) -> AlgorithmVehicleType:
        url_to_resource = "vehicles/types/{0}".format(vehicle_type_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert(AlgorithmVehicleType, response_dict)

    def get_links(self, time_window: TimeWindow) -> List[AlgorithmLink]:
        url_to_resource = "links"
        query_parameters = object_to_algorithm_platform_json_converter.convert_any_object(time_window)
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_link, response_dict)

    def get_links_containing_any_node(self, time_window: TimeWindow, node_ids: List[int]) -> List[AlgorithmLink]:
        url_to_resource = "links"
        manual_converted_query_parameters = dict(nodeFilter=node_ids)
        query_parameters = merge_query_parameters(
            [manual_converted_query_parameters,
             object_to_algorithm_platform_json_converter.convert_any_object(time_window)])
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_link, response_dict)

    def get_connection_links(self, time_window: TimeWindow) -> List[AlgorithmConnectionLink]:
        url_to_resource = "links"
        query_parameters = merge_query_parameters(
            [dict(linkType=object_to_algorithm_platform_json_converter.convert_any_object(LinkType.connection)),
             object_to_algorithm_platform_json_converter.convert_any_object(time_window)])
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_link, response_dict)

    def get_connection_links_containing_any_node(self, time_window: TimeWindow, node_ids: List[int]
                                                 ) -> List[AlgorithmConnectionLink]:
        url_to_resource = "links"
        manual_converted_query_parameters = dict(nodeFilter=node_ids)
        query_parameters = merge_query_parameters(
            [manual_converted_query_parameters,
             dict(linkType=object_to_algorithm_platform_json_converter.convert_any_object(LinkType.connection)),
             object_to_algorithm_platform_json_converter.convert_any_object(time_window)])
        response_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)
        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_link, response_dict)

    def calculate_run_times(self, train_id: int) -> (UpdateTimesTrain, None):
        url_to_resource = "services/trains/{0}:run-time-calculation".format(train_id)
        response_dict = self.__communication_layer.do_get_request(url_to_resource)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_update_train_times(response_dict)

    def notify_user(self, title: str, description: str) -> None:
        url_to_resource = 'user-outputs/notifications'
        request_body = dict(title=title, description=description)
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def show_status_message(self, status_message: str, log_message: Optional[str] = None) -> None:
        url_to_resource = 'user-outputs/status-messages'
        request_body = dict(statusMessage=status_message, logMessage=log_message)
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def create_table(self, table_definition: TableDefinition) -> int:
        url_to_resource = 'user-outputs/tables'
        table_definition_as_json = object_to_algorithm_platform_json_converter.convert_any_object(table_definition)
        for column_index in range(len(table_definition_as_json["columns"])):
            table_definition_as_json["columns"][column_index]["header"] = \
                table_definition_as_json["columns"][column_index]["header"]["value"]
        response_dict = self.__communication_layer.do_post_request(url_to_resource, table_definition_as_json)
        return converter_helpers.convert_keys_to_snake_case(response_dict)["table_id"]

    def add_rows_to_table(self, table_id: int, table_rows: List[TableRow]):
        url_to_resource = 'user-outputs/tables/{0}/rows'.format(table_id)
        list_of_cells_per_row = object_to_algorithm_platform_json_converter.convert_any_object(table_rows)
        request_body = [dict(row=row["cells"]) for row in list_of_cells_per_row]
        self.__communication_layer.do_post_request(url_to_resource, request_body)

    def __delegate_get_any_parameter(
            self,
            key: str
    ) -> Union[
        AlgorithmTrain,
        TimeWindow,
        bool,
        int,
        str,
        list,
        dict
    ]:
        url_to_resource = "parameters/{0}".format(key)
        return self.__communication_layer.do_get_request(url_to_resource)["value"]

    def get_bool_algorithm_parameter(self, key: str) -> bool:
        return self.__delegate_get_any_parameter(key)

    def get_int_algorithm_parameter(self, key: str) -> int:
        return self.__delegate_get_any_parameter(key)

    def get_string_algorithm_parameter(self, key: str) -> str:
        return self.__delegate_get_any_parameter(key)

    def get_algorithm_train_parameter(self, key: str) -> AlgorithmTrain:
        response_dict = self.__delegate_get_any_parameter(key)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train(response_dict)

    def get_algorithm_trains_parameter(self, key: str) -> List[AlgorithmTrain]:
        response_list = self.__delegate_get_any_parameter(key)

        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_train,
            response_list
        )

    def get_time_window_algorithm_parameter(self, key: str) -> TimeWindow:
        response_dict = self.__delegate_get_any_parameter(key)
        return algorithm_platform_json_to_aidm_converter.convert_json_to_time_window(response_dict)

    def get_node_track_closures(
            self,
            time_window: TimeWindow
    ) -> List[AlgorithmNodeTrackClosure]:
        url_to_resource = 'possessions/node-track-closures'
        query_parameters = object_to_algorithm_platform_json_converter.convert_any_object(time_window)
        response_list_of_dict = self.__communication_layer.do_get_request(url_to_resource, query_parameters)

        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_node_track_closure,
            response_list_of_dict
        )

    def get_section_track_closures(
            self,
            time_window: TimeWindow
    ) -> List[AlgorithmSectionTrackClosure]:
        request_parameters = object_to_algorithm_platform_json_converter.convert_any_object(time_window)
        url_to_resource = 'possessions/section-track-closures'
        response_list_of_dict = self.__communication_layer.do_get_request(url_to_resource, request_parameters)

        return algorithm_platform_json_to_aidm_converter.convert_list(
            algorithm_platform_json_to_aidm_converter.convert_json_to_algorithm_section_track_closure,
            response_list_of_dict
        )
