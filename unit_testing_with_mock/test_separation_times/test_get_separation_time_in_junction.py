import datetime
import unittest
from unittest import mock

import AlgorithmInterfaceFactory
import unit_testing_with_mock.SessionMockFactory as SessionMockFactory
import unit_testing_with_mock.unit_testing_helpers
from unit_testing_with_mock.unit_testing_helpers import get_api_url


class TestGetSeparationTimeInJunction(unittest.TestCase):
    class GetSeparationTimeInJunctionTestMockSession(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "separationTime": "PT5M"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterfaceFactory.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInJunctionTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInJunctionTestMockSession)
    def test_get_separation_time_in_junction_request(self, mocked_get_obj):
        proceeding_train_path_node_id = 4246
        succeeding_train_path_node_id = 5702

        self.interface_to_viriato.get_separation_time_in_junction(proceeding_train_path_node_id,
                                                                  succeeding_train_path_node_id)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSeparationTimeInJunctionTestMockSession__last_request,
                         get_api_url() + "/junction-separation-time/between-train-path-nodes/4246/5702")
        self.assertDictEqual(session_obj._GetSeparationTimeInJunctionTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInJunctionTestMockSession)
    def test_get_separation_time_in_junction_response(self, mocked_get_obj):
        proceeding_train_path_node_id = 4246
        succeeding_train_path_node_id = 5702

        separation_time = self.interface_to_viriato.get_separation_time_in_junction(proceeding_train_path_node_id,
                                                                  succeeding_train_path_node_id)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(minutes=5))

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInJunctionTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
