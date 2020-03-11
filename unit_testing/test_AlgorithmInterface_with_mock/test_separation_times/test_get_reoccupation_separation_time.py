import datetime
import unittest
from unittest import mock

import AlgorithmInterface.AlgorithmInterface
import unit_testing.test_AlgorithmInterface_with_mock.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_with_mock_helpers import get_api_url, \
    SessionMockTestBase


class TestGetReoccupationSeparationTime(unittest.TestCase):
    class GetReoccupationSeparationTimeTestMockSession(SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "separationTime": "PT50S"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetReoccupationSeparationTimeTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetReoccupationSeparationTimeTestMockSession)
    def test_get_headway_time_for_train_path_nodes_request(self, mocked_get_obj):
        proceeding_train_path_node_id = 9999
        succeeding_train_path_node_id = 1
        train_id = 322

        self.interface_to_viriato.get_station_track_reoccupation_separation_time(proceeding_train_path_node_id,
                                                                                 succeeding_train_path_node_id,
                                                                                 train_id)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetReoccupationSeparationTimeTestMockSession__last_request,
                         get_api_url() + "/station-track-reoccupation-separation-time/9999/1/322")
        self.assertDictEqual(session_obj._GetReoccupationSeparationTimeTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetReoccupationSeparationTimeTestMockSession)
    def test_get_headway_time_for_train_path_nodes_response(self, mocked_get_obj):
        proceeding_train_path_node_id = 9999
        succeeding_train_path_node_id = 1
        train_id = 322

        separation_time = self.interface_to_viriato.get_station_track_reoccupation_separation_time(
            proceeding_train_path_node_id, succeeding_train_path_node_id, train_id)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(seconds=50))

    @mock.patch('requests.Session', side_effect=GetReoccupationSeparationTimeTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
