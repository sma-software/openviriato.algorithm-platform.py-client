import datetime
import unittest
from unittest import mock
from py_client.aidm import IncomingRoutingEdge, OutgoingRoutingEdge, StopStatus
import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetSeparationTimeInStationForRoutes(unittest.TestCase):
    class GetSeparationTimeInStationForRoutesTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            incoming_incoming_case_parameters = dict(
                PrecedingFromSectionTrackID=1000,
                PrecedingToNodeTrackID=1,
                PrecedingStopStatus='Passing',
                SucceedingFromSectionTrackID=1000,
                SucceedingToNodeTrackID=1,
                SucceedingStopStatus='CommercialStop')

            incoming_outgoing_case_parameters = dict(
                PrecedingFromSectionTrackID=999,
                PrecedingToNodeTrackID=1,
                PrecedingStopStatus='OperationalStop',
                SucceedingToSectionTrackID=324,
                SucceedingFromNodeTrackID=500,
                SucceedingStopStatus='Passing')

            outgoing_incoming_case_parameters = dict(
                PrecedingToSectionTrackID=1,
                PrecedingFromNodeTrackID=2,
                PrecedingStopStatus='CommercialStop',
                SucceedingFromSectionTrackID=3,
                SucceedingToNodeTrackID=4,
                SucceedingStopStatus='Passing')

            outgoing_outgoing_case_parameters = dict(
                PrecedingToSectionTrackID=100,
                PrecedingFromNodeTrackID=150,
                PrecedingStopStatus='OperationalStop',
                SucceedingToSectionTrackID=200,
                SucceedingFromNodeTrackID=250,
                SucceedingStopStatus='CommercialStop')

            if self.__last_body == incoming_incoming_case_parameters:
                json_string = """{ "separationTime": "PT24S"}"""
                return SessionMockFactory.create_response_mock(json_string, 200)
            elif self.__last_body == incoming_outgoing_case_parameters:
                json_string = """{ "separationTime": "PT2M"}"""
                return SessionMockFactory.create_response_mock(json_string, 200)
            elif self.__last_body == outgoing_incoming_case_parameters:
                json_string = """{ "separationTime": null}"""
                return SessionMockFactory.create_response_mock(json_string, 200)
            elif self.__last_body == outgoing_outgoing_case_parameters:
                json_string = """{ "separationTime": "PT5M"}"""
                return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_request(self, mocked_get_obj):
        preceding_routing_edge = IncomingRoutingEdge(node_id=12, end_node_track_id=1, start_section_track_id=999)
        preceding_stop_status = StopStatus['operational_stop']
        succeeding_routing_edge = OutgoingRoutingEdge(node_id=12, start_node_track_id=500, end_section_track_id=324)
        succeeding_stop_status = StopStatus['passing']

        self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge,
            preceding_stop_status,
            succeeding_routing_edge,
            succeeding_stop_status)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(
            session_obj._GetSeparationTimeInStationForRoutesTestMockSession__last_request,
            get_api_url() + '/nodes/12/separation-times')

        expected_query_parameters = dict(
            PrecedingFromSectionTrackID=999,
            PrecedingToNodeTrackID=1,
            PrecedingStopStatus='OperationalStop',
            SucceedingFromNodeTrackID=500,
            SucceedingToSectionTrackID=324,
            SucceedingStopStatus='Passing')
        self.assertDictEqual(
            session_obj._GetSeparationTimeInStationForRoutesTestMockSession__last_body,
            expected_query_parameters)

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_incoming_incoming(self, mocked_get_obj):
        preceding_routing_edge = IncomingRoutingEdge(node_id=12, end_node_track_id=1, start_section_track_id=1000)
        preceding_stop_status = StopStatus['passing']
        succeeding_routing_edge = IncomingRoutingEdge(node_id=12, end_node_track_id=1, start_section_track_id=1000)
        succeeding_stop_status = StopStatus['commercial_stop']

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge,
            preceding_stop_status,
            succeeding_routing_edge,
            succeeding_stop_status)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(seconds=24))

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_incoming_outgoing(self, mocked_get_obj):
        preceding_routing_edge = IncomingRoutingEdge(node_id=12, end_node_track_id=1, start_section_track_id=999)
        preceding_stop_status = StopStatus['operational_stop']
        succeeding_routing_edge = OutgoingRoutingEdge(node_id=12, start_node_track_id=500, end_section_track_id=324)
        succeeding_stop_status = StopStatus['passing']

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge,
            preceding_stop_status,
            succeeding_routing_edge,
            succeeding_stop_status)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(seconds=120))

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_outgoing_incoming(self, mocked_get_obj):
        preceding_routing_edge = OutgoingRoutingEdge(node_id=111, start_node_track_id=2, end_section_track_id=1)
        preceding_stop_status = StopStatus['commercial_stop']
        succeeding_routing_edge = IncomingRoutingEdge(node_id=111, end_node_track_id=4, start_section_track_id=3)
        succeeding_stop_status = StopStatus['passing']

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge,
            preceding_stop_status,
            succeeding_routing_edge,
            succeeding_stop_status)

        self.assertIsNone(separation_time)

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_outgoing_outgoing(self, mocked_get_obj):
        preceding_routing_edge = OutgoingRoutingEdge(node_id=12, start_node_track_id=150, end_section_track_id=100)
        preceding_stop_status = StopStatus['operational_stop']
        succeeding_routing_edge = OutgoingRoutingEdge(node_id=12, start_node_track_id=250, end_section_track_id=200)
        succeeding_stop_status = StopStatus['commercial_stop']

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge,
            preceding_stop_status,
            succeeding_routing_edge,
            succeeding_stop_status)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(seconds=300))

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
