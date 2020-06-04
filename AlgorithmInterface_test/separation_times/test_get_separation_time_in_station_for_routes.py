import datetime
import unittest
from unittest import mock
from AIDMClasses import IncomingRoutingEdge, OutgoingRoutingEdge, StopStatus
import AlgorithmInterface.AlgorithmInterface
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetSeparationTimeInStationForRoutes(unittest.TestCase):
    class GetSeparationTimeInStationForRoutesTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            incoming_incoming_case_parameters = dict(
                PrecedingFromSectionTrackID=1000,
                PrecedingToNodeTrackID=1,
                PrecedingStopStatus='passing',
                SucceedingFromSectionTrackID=1000,
                SucceedingToNodeTrackID=1,
                SucceedingStopStatus='commercialStop')

            incoming_outgoing_case_parameters = dict(
                PrecedingFromSectionTrackID=999,
                PrecedingToNodeTrackID=1,
                PrecedingStopStatus='operationalStop',
                SucceedingToSectionTrackID=324,
                SucceedingFromNodeTrackID=500,
                SucceedingStopStatus='passing')

            outgoing_incoming_case_parameters = dict(
                PrecedingToSectionTrackID=1,
                PrecedingFromNodeTrackID=2,
                PrecedingStopStatus='commercialStop',
                SucceedingFromSectionTrackID=3,
                SucceedingToNodeTrackID=4,
                SucceedingStopStatus='passing')

            outgoing_outgoing_case_parameters = dict(
                PrecedingToSectionTrackID=100,
                PrecedingFromNodeTrackID=150,
                PrecedingStopStatus='operationalStop',
                SucceedingToSectionTrackID=200,
                SucceedingFromNodeTrackID=250,
                SucceedingStopStatus='commercialStop')

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

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_request(self, mocked_get_obj):
        preceding_routing_edge = IncomingRoutingEdge(NodeID=12, EndNodeTrackID=1, StartSectionTrackID=999)
        preceding_stop_status = StopStatus['operationalStop']
        succeeding_routing_edge = OutgoingRoutingEdge(NodeID=12, StartNodeTrackID=500, EndSectionTrackID=324)
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
            PrecedingStopStatus='operationalStop',
            SucceedingFromNodeTrackID=500,
            SucceedingToSectionTrackID=324,
            SucceedingStopStatus='passing')
        self.assertDictEqual(
            session_obj._GetSeparationTimeInStationForRoutesTestMockSession__last_body,
            expected_query_parameters)

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_incoming_incoming(self, mocked_get_obj):
        preceding_routing_edge = IncomingRoutingEdge(NodeID=12, EndNodeTrackID=1, StartSectionTrackID=1000)
        preceding_stop_status = StopStatus['passing']
        succeeding_routing_edge = IncomingRoutingEdge(NodeID=12, EndNodeTrackID=1, StartSectionTrackID=1000)
        succeeding_stop_status = StopStatus['commercialStop']

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge,
            preceding_stop_status,
            succeeding_routing_edge,
            succeeding_stop_status)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(seconds=24))

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_incoming_outgoing(self, mocked_get_obj):
        preceding_routing_edge = IncomingRoutingEdge(NodeID=12, EndNodeTrackID=1, StartSectionTrackID=999)
        preceding_stop_status = StopStatus['operationalStop']
        succeeding_routing_edge = OutgoingRoutingEdge(NodeID=12, StartNodeTrackID=500, EndSectionTrackID=324)
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
        preceding_routing_edge = OutgoingRoutingEdge(NodeID=111, StartNodeTrackID=2, EndSectionTrackID=1)
        preceding_stop_status = StopStatus['commercialStop']
        succeeding_routing_edge = IncomingRoutingEdge(NodeID=111, EndNodeTrackID=4, StartSectionTrackID=3)
        succeeding_stop_status = StopStatus['passing']

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_routes(
            preceding_routing_edge,
            preceding_stop_status,
            succeeding_routing_edge,
            succeeding_stop_status)

        self.assertIsNone(separation_time)

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForRoutesTestMockSession)
    def test_get_separation_time_in_station_for_routes_response_outgoing_outgoing(self, mocked_get_obj):
        preceding_routing_edge = OutgoingRoutingEdge(NodeID=12, StartNodeTrackID=150, EndSectionTrackID=100)
        preceding_stop_status = StopStatus['operationalStop']
        succeeding_routing_edge = OutgoingRoutingEdge(NodeID=12, StartNodeTrackID=250, EndSectionTrackID=200)
        succeeding_stop_status = StopStatus['commercialStop']

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
