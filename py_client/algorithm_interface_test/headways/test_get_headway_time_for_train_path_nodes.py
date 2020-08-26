import datetime
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetHeadwayTimeForTrainPathNodes(unittest.TestCase):
    class GetHeadwayTimeForTrainPathNodesTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "separationTime": "PT2M"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeForTrainPathNodesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeForTrainPathNodesTestMockSession)
    def test_get_headway_time_for_train_path_nodes_request(self, mocked_get_obj):
        proceeding_node_id = 4246
        succeeding_node_id = 7158

        self.interface_to_viriato.get_headway_time_for_train_path_nodes(proceeding_node_id, succeeding_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetHeadwayTimeForTrainPathNodesTestMockSession__last_request,
                         get_api_url() + "/headway-times/between-train-path-nodes/4246/7158")
        self.assertDictEqual(session_obj._GetHeadwayTimeForTrainPathNodesTestMockSession__last_body, {})

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeForTrainPathNodesTestMockSession)
    def test_get_headway_time_for_train_path_nodes_response(self, mocked_get_obj):
        proceeding_node_id = 4246
        succeeding_node_id = 7158

        separation_time = self.interface_to_viriato.get_headway_time_for_train_path_nodes(proceeding_node_id,
                                                                                          succeeding_node_id)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(minutes=2))

    @mock.patch('requests.Session', side_effect=GetHeadwayTimeForTrainPathNodesTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
