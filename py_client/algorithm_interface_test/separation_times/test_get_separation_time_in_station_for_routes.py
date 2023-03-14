from datetime import timedelta
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import IncomingRoutingEdge, OutgoingRoutingEdge, StopStatus, IncomingNodeTrackRoutingEdge, OutgoingNodeTrackRoutingEdge
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetSeparationTimeInStationForRoutes(unittest.TestCase):
    class GetSeparationTimeInStationForRoutesTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self._last_body = params
            self._last_request = request

            incoming_incoming_case_parameters = dict(
                precedingFromSectionTrackId=1000, precedingStopStatus="passing", succeedingFromSectionTrackId=1000, succeedingStopStatus="commercialStop"
            )

            incoming_outgoing_case_parameters = dict(
                precedingFromSectionTrackId=999,
                precedingToNodeTrackId=12215,
                succeedingToSectionTrackId=324,
                precedingStopStatus="operationalStop",
                succeedingStopStatus="passing",
            )

            outgoing_incoming_case_parameters = dict(
                precedingToSectionTrackId=1, precedingStopStatus="commercialStop", succeedingFromSectionTrackId=3, succeedingStopStatus="passing"
            )

            outgoing_outgoing_case_parameters = dict(
                precedingToSectionTrackId=915,
                precedingFromNodeTrackId=150,
                precedingStopStatus="operationalStop",
                succeedingToSectionTrackId=200,
                succeedingStopStatus="commercialStop",
            )

            if self._last_body == incoming_incoming_case_parameters:
                json_string = """{ "separationTime": "PT24S"}"""
                return SessionMockFactory.create_response_mock(json_string, 200)
            elif self._last_body == incoming_outgoing_case_parameters:
                json_string = """{ "separationTime": "PT2M"}"""
                return SessionMockFactory.create_response_mock(json_string, 200)
            elif self._last_body == outgoing_incoming_case_parameters:
                json_string = """{ "separationTime": null}"""
                return SessionMockFactory.create_response_mock(json_string, 200)
            elif self._last_body == outgoing_outgoing_case_parameters:
                json_string = """{ "separationTime": "PT5M"}"""
                return SessionMockFactory.create_response_mock(json_string, 200)
            else:
                return SessionMockFactory.create_response_mock("No corresponding TestCase in Mock", 400)

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_request(self, mocked_get_obj):
        preceding_routing_edge = IncomingNodeTrackRoutingEdge(node_id=12, end_node_track_id=12215, start_section_track_id=999)
        preceding_stop_status = StopStatus.operational_stop
        succeeding_routing_edge = OutgoingRoutingEdge(node_id=12, end_section_track_id=324)
        succeeding_stop_status = StopStatus.passing

        self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge, preceding_stop_status, succeeding_routing_edge, succeeding_stop_status
        )

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/nodes/12/separation-times")

        expected_query_parameters = dict(
            precedingFromSectionTrackId=999,
            precedingToNodeTrackId=12215,
            precedingStopStatus="operationalStop",
            succeedingToSectionTrackId=324,
            succeedingStopStatus="passing",
        )
        self.assertDictEqual(session_obj.last_body, expected_query_parameters)

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_incoming_incoming(self, mocked_get_obj):
        preceding_routing_edge = IncomingRoutingEdge(node_id=12, start_section_track_id=1000)
        preceding_stop_status = StopStatus.passing
        succeeding_routing_edge = IncomingRoutingEdge(node_id=12, start_section_track_id=1000)
        succeeding_stop_status = StopStatus.commercial_stop

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge, preceding_stop_status, succeeding_routing_edge, succeeding_stop_status
        )

        self.assertIsInstance(separation_time, timedelta)
        self.assertEqual(separation_time, timedelta(seconds=24))

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_incoming_outgoing(self, mocked_get_obj):
        preceding_routing_edge = IncomingNodeTrackRoutingEdge(node_id=12, end_node_track_id=12215, start_section_track_id=999)
        preceding_stop_status = StopStatus.operational_stop
        succeeding_routing_edge = OutgoingRoutingEdge(node_id=12, end_section_track_id=324)
        succeeding_stop_status = StopStatus.passing

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge, preceding_stop_status, succeeding_routing_edge, succeeding_stop_status
        )

        self.assertIsInstance(separation_time, timedelta)
        self.assertEqual(separation_time, timedelta(seconds=120))

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_outgoing_incoming(self, mocked_get_obj):
        preceding_routing_edge = OutgoingRoutingEdge(node_id=111, end_section_track_id=1)
        preceding_stop_status = StopStatus.commercial_stop
        succeeding_routing_edge = IncomingRoutingEdge(node_id=111, start_section_track_id=3)
        succeeding_stop_status = StopStatus.passing

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge, preceding_stop_status, succeeding_routing_edge, succeeding_stop_status
        )

        self.assertIsNone(separation_time)

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_outgoing_outgoing(self, mocked_get_obj):
        preceding_routing_edge = OutgoingNodeTrackRoutingEdge(node_id=12, start_node_track_id=150, end_section_track_id=915)
        preceding_stop_status = StopStatus.operational_stop
        succeeding_routing_edge = OutgoingRoutingEdge(node_id=12, end_section_track_id=200)
        succeeding_stop_status = StopStatus.commercial_stop

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge, preceding_stop_status, succeeding_routing_edge, succeeding_stop_status
        )

        self.assertIsInstance(separation_time, timedelta)
        self.assertEqual(separation_time, timedelta(seconds=300))

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
