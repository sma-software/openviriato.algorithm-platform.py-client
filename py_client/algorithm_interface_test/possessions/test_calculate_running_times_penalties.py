import unittest
from unittest import mock
from datetime import timedelta

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm import RunningTimePenaltyOnTrainPath

class TestCalculateRunningTimesPenalties(unittest.TestCase):
    class CalculateRunningTimePenaltiesMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = ( "[{\n"
                            "   \"possessionId\": 6745, \n"
                            "   \"fromTrainPathNodeId\": 6738, \n"
                            "   \"toTrainPathNodeId\": 6739, \n"
                            "   \"requiredRunningTimePenalty\": \"PT2M\" \n"
                            " }\n"
                            "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=CalculateRunningTimePenaltiesMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CalculateRunningTimePenaltiesMockSession)
    def test_calculate_running_time_penalties(self, mocked_get_obj):
        train_id = 6740
        self.interface_to_viriato.calculate_running_time_penalties_on_train(train_id = train_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._CalculateRunningTimePenaltiesMockSession__last_request,
                         get_api_url() + "/services/trains/{}:calculate-running-time-penalties".format(train_id))

        self.assertDictEqual(session_obj._CalculateRunningTimePenaltiesMockSession__last_body,
                             dict())

    @mock.patch('requests.Session', side_effect=CalculateRunningTimePenaltiesMockSession)
    def test_calculate_running_time_penalties_response(self, mocked_get_obj):
        train_id = 6740

        list_of_running_time_penalties = self.interface_to_viriato.calculate_running_time_penalties_on_train(train_id = train_id)

        self.assertIsInstance(
            list_of_running_time_penalties,
            list)
        self.assertIsInstance(
            list_of_running_time_penalties[0],
            RunningTimePenaltyOnTrainPath)
        self.assertEqual(
            list_of_running_time_penalties[0].possession_id,
            6745)
        self.assertEqual(
            list_of_running_time_penalties[0].from_train_path_node_id,
            6738)
        self.assertEqual(
            list_of_running_time_penalties[0].to_train_path_node_id,
            6739)
        self.assertEqual(
            list_of_running_time_penalties[0].required_running_time_penalty,
            timedelta(minutes = 2))


    @mock.patch('requests.Session', side_effect=CalculateRunningTimePenaltiesMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)

class TestCalculateRunningTimesPenaltiesEmpty(unittest.TestCase):
    class CalculateRunningTimePenaltiesEmptyMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = "[]"

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=CalculateRunningTimePenaltiesEmptyMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=CalculateRunningTimePenaltiesEmptyMockSession)
    def test_calculate_running_time_penalties_empty(self, mocked_get_obj):
        train_id = 6740

        list_of_running_time_penalties = self.interface_to_viriato.calculate_running_time_penalties_on_train(train_id=train_id)

        self.assertIsInstance(
            list_of_running_time_penalties,
            list)

        self.assertEqual(list_of_running_time_penalties.__len__(), 0)

    @mock.patch('requests.Session', side_effect=CalculateRunningTimePenaltiesEmptyMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)