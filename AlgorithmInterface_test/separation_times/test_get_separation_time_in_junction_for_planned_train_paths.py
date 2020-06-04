import datetime
import unittest
from unittest import mock
import AlgorithmInterface.AlgorithmInterface
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import get_api_url,  SessionMockTestBase


class TestGetSeparationTimeInJunctionForPlannedTrainPaths(unittest.TestCase):
    class GetSeparationTimeInJunctionForPlannedTrainPathsTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            five_minute_case_parameters = dict(PrecedingTrainPathNodeID=4246, SucceedingTrainPathNodeID=5702)
            null_case_parameters = dict(PrecedingTrainPathNodeID=1, SucceedingTrainPathNodeID=1)

            if self.__last_body == five_minute_case_parameters:
                json_string = """{ "separationTime": "PT5M"}"""
                return SessionMockFactory.create_response_mock(json_string, 200)
            elif self.__last_body == null_case_parameters:
                json_string = """{ "separationTime": null}"""
                return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInJunctionForPlannedTrainPathsTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInJunctionForPlannedTrainPathsTestMockSession)
    def test_get_separation_time_in_junction_for_planned_train_paths_request(self, mocked_get_obj):
        node_id = 123
        proceeding_train_path_node_id = 4246
        succeeding_train_path_node_id = 5702

        self.interface_to_viriato.get_separation_time_in_junction_for_planned_train_paths(
            node_id,
            proceeding_train_path_node_id,
            succeeding_train_path_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(
            session_obj._GetSeparationTimeInJunctionForPlannedTrainPathsTestMockSession__last_request,
            get_api_url() + "/nodes/123/separation-times")

        expected_query_parameters = dict(PrecedingTrainPathNodeID=4246, SucceedingTrainPathNodeID=5702)
        self.assertDictEqual(
            session_obj._GetSeparationTimeInJunctionForPlannedTrainPathsTestMockSession__last_body,
            expected_query_parameters)

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInJunctionForPlannedTrainPathsTestMockSession)
    def test_get_separation_time_in_junction_response_five_minutes(self, mocked_get_obj):
        node_id = 123
        proceeding_train_path_node_id = 4246
        succeeding_train_path_node_id = 5702

        separation_time = self.interface_to_viriato.get_separation_time_in_junction_for_planned_train_paths(
            node_id,
            proceeding_train_path_node_id,
            succeeding_train_path_node_id)

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(minutes=5))

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInJunctionForPlannedTrainPathsTestMockSession)
    def test_get_separation_time_in_junction_response_none(self, mocked_get_obj):
        node_id = 123
        proceeding_train_path_node_id = 1
        succeeding_train_path_node_id = 1

        separation_time = self.interface_to_viriato.get_separation_time_in_junction_for_planned_train_paths(
            node_id,
            proceeding_train_path_node_id,
            succeeding_train_path_node_id)

        self.assertIsNone(separation_time)

    @mock.patch('requests.Session', side_effect=GetSeparationTimeInJunctionForPlannedTrainPathsTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
