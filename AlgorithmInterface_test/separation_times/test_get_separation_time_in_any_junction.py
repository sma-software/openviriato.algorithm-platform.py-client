import datetime
import unittest
from unittest import mock

import AlgorithmInterface.AlgorithmInterface
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetSeparationTimeInAnyJunction(unittest.TestCase):
    class GetSeparationTimeInAnyJunctionTestMockSession(SessionMockTestBase):
        # to replace session.get:
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "separationTime": "P1D"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInAnyJunctionTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInAnyJunctionTestMockSession)
    def test_get_separation_time_in_any_junction_request(self, mocked_get_obj):
        preceding_train_path_node_id = 80
        succeeding_train_path_node_id = 324
        node_id = 123
        preceding_route_start_id = 1
        preceding_route_end_id = 12
        succeeding_route_start_id = 178
        succeeding_route_end_id = 12740

        self.interface_to_viriato.get_separation_time_in_any_junction(preceding_train_path_node_id,
                                                                      succeeding_train_path_node_id,
                                                                      node_id,
                                                                      preceding_route_start_id,
                                                                      preceding_route_end_id,
                                                                      succeeding_route_start_id,
                                                                      succeeding_route_end_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSeparationTimeInAnyJunctionTestMockSession__last_request,
                         get_api_url() + '/junction-separation-time/between-train-path-nodes/80/324/for-node/123' +
                         '/preceding-route/1/12/succeeding-route/178/12740')
        self.assertDictEqual(session_obj._GetSeparationTimeInAnyJunctionTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInAnyJunctionTestMockSession)
    def test_test_get_separation_time_in_any_junction_response(self, mocked_get_obj):
        preceding_train_path_node_id = 0
        succeeding_train_path_node_id = 0
        node_id = 0
        preceding_route_start_id = 0
        preceding_route_end_id = 0
        succeeding_route_start_id = 0
        succeeding_route_end_id = 0

        separation_time = self.interface_to_viriato.get_separation_time_in_any_junction(preceding_train_path_node_id,
                                                                                        succeeding_train_path_node_id,
                                                                                        node_id,
                                                                                        preceding_route_start_id,
                                                                                        preceding_route_end_id,
                                                                                        succeeding_route_start_id,
                                                                                        succeeding_route_end_id)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(days=1))

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInAnyJunctionTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
