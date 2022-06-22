import datetime
import unittest
from unittest import mock
from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm.aidm_conflict import ConflictDetectionArguments, AlgorithmNodeConflict, _AlgorithmOneTrainNodeConflict, ConflictType
from py_client.aidm.aidm_time_window_classes import TimeWindow


class TestDetectConflicts(unittest.TestCase):
    class DetectConflictsMockSession(SessionMockTestBase):
        def get(self, request, params, json):
            self.__last_body = json
            self.__last_params = params
            self.__last_request = request

            json_string = ( "["
                            "   {"
                            "       \"conflictType\": \"changeDirection\", \n"
                            "       \"timeWindow\": { \n"
                            "           \"fromTime\": \"2022-04-14T11:42:10\", \n"
                            "           \"toTime\": \"2022-04-14T12:02:00\" \n"
                            "   }, \n"
                            "   \"nodeId\": 892, \n"
                            "   \"trainId\": 2743, \n"
                            "   \"trainPathNodeId\": 227 \n"
                            "    } \n"
                            "]"
                            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_mock_session(self, mocked_get_obj):
        train_ids = [2743]
        arguments = ConflictDetectionArguments(train_ids=train_ids)

        self.interface_to_viriato.detect_conflicts(arguments=arguments)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._DetectConflictsMockSession__last_request,
                         get_api_url() + "/services/trains:detect-conflicts")

        self.assertDictEqual(session_obj._DetectConflictsMockSession__last_body, {'trainIds': [2743], 'filters': {'location': {'nodeIds': None, 'sectionTrackIds': None}, 'conflictTypes': None}})
        self.assertDictEqual(session_obj._DetectConflictsMockSession__last_params, {})

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_response(self, mocked_get_obj):
        arguments = ConflictDetectionArguments(train_ids = [6745, 6750])
        list_of_algorithm_conflicts = self.interface_to_viriato.detect_conflicts(arguments=arguments)

        self.assertIsInstance(
            list_of_algorithm_conflicts,
            list)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0],
            AlgorithmNodeConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0],
            _AlgorithmOneTrainNodeConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0].conflict_type,
            ConflictType)

        self.assertEqual(
            list_of_algorithm_conflicts[0].conflict_type,
            ConflictType.ChangeDirection)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0].time_window,
            TimeWindow)

        self.assertEqual(
            list_of_algorithm_conflicts[0].time_window.from_time,
            datetime.datetime(day=14, month=4, year=2022, hour=11, minute=42, second=10))

        self.assertEqual(
            list_of_algorithm_conflicts[0].time_window.to_time,
            datetime.datetime(day=14, month=4, year=2022, hour=12, minute=2, second=0))

        self.assertEqual(
            list_of_algorithm_conflicts[0].node_id,
            892)

        self.assertEqual(
            list_of_algorithm_conflicts[0].train_id,
            2743)

        self.assertEqual(
            list_of_algorithm_conflicts[0].train_path_node_id,
            227)

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
