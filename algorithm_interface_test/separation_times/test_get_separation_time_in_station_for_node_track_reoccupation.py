import datetime
import unittest
from unittest import mock
import algorithm_interface.algorithm_interface
import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetSeparationTimeInStationForNodeTrackReoccupation(unittest.TestCase):
    class GetSeparationTimeInStationForNodeTrackReoccupationTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "separationTime": "PT50S"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForNodeTrackReoccupationTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForNodeTrackReoccupationTestMockSession)
    def test_get_separation_time_in_station_for_node_track_reoccupation_request(self, mocked_get_obj):
        node_id = 1123
        node_track_id = 123
        self.interface_to_viriato.get_separation_time_in_station_for_node_track_reoccupation(node_id, node_track_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(
            session_obj._GetSeparationTimeInStationForNodeTrackReoccupationTestMockSession__last_request,
            get_api_url() + "/nodes/1123/separation-times")
        self.assertDictEqual(
            session_obj._GetSeparationTimeInStationForNodeTrackReoccupationTestMockSession__last_body,
            dict(NodeTrackID=123))

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForNodeTrackReoccupationTestMockSession)
    def test_get_separation_time_in_station_for_node_track_reoccupation_response(self, mocked_get_obj):
        node_id = 1123
        node_track_id = 123

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_node_track_reoccupation(
            node_id,
            node_track_id)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(seconds=50))

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInStationForNodeTrackReoccupationTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)