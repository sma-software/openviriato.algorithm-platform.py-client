from datetime import datetime
import unittest
from unittest import mock

from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm.aidm_conflict import (
    ConflictType,
    ConflictDetectionArguments,
    AlgorithmMultipleTrainsConflict,
    AlgorithmNodeConflict,
)
from py_client.aidm.aidm_time_window_classes import TimeWindow


class TestDetectConflicts(unittest.TestCase):
    class DetectConflictsMockSession(SessionMockTestBase):
        def get(self, request, params, json):
            self.__last_body = json
            self.__last_params = params
            self.__last_request = request

            json_string = (
                "["
                "   {"
                '       "conflictType": "congestedNode", \n'
                '       "nodeID": 12, \n'
                '       "timeWindow": { \n'
                '           "fromTime": "2005-05-01T04:04:00", \n'
                '           "toTime": "2005-05-01T04:07:00" \n'
                "       }, \n"
                '       "involvedTrainPathNodeReferences": [ \n'
                "           { \n"
                '               "trainId": 1234, \n'
                '               "trainPathNodeId": 12345 \n'
                "           }, \n"
                "           { \n"
                '               "trainId": 1235, \n'
                '               "trainPathNodeId": 12346 \n'
                "           }, \n"
                "           { \n"
                '               "trainId": 1236, \n'
                '               "trainPathNodeId": 12347 \n'
                "           } \n"
                "       ] \n"
                "    } \n"
                "]"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_mock_session(self, mocked_get_obj):
        train_ids = [1234, 1235, 1236]
        arguments = ConflictDetectionArguments(train_ids=train_ids).with_type_filter([ConflictType.CongestedNode])
        self.interface_to_viriato.detect_conflicts(arguments=arguments)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._DetectConflictsMockSession__last_request, get_api_url() + "/services/trains:detect-conflicts")

        self.assertDictEqual(
            session_obj._DetectConflictsMockSession__last_body,
            {"trainIds": [1234, 1235, 1236], "filters": {"location": {"nodeIds": None, "sectionTrackIds": None}, "conflictTypes": ["congestedNode"]}},
        )
        self.assertDictEqual(session_obj._DetectConflictsMockSession__last_params, {})

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_response(self, mocked_get_obj):
        arguments = ConflictDetectionArguments(train_ids=[1234, 1235, 1236])
        list_of_algorithm_conflicts = self.interface_to_viriato.detect_conflicts(arguments=arguments)

        self.assertIsInstance(list_of_algorithm_conflicts, list)

        self.assertIsInstance(list_of_algorithm_conflicts[0], AlgorithmNodeConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[0], AlgorithmMultipleTrainsConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[0].conflict_type, ConflictType)
        self.assertEqual(list_of_algorithm_conflicts[0].conflict_type, ConflictType.CongestedNode)
        self.assertEqual(list_of_algorithm_conflicts[0].node_id, 12)
        self.assertIsInstance(list_of_algorithm_conflicts[0].time_window, TimeWindow)
        self.assertEqual(list_of_algorithm_conflicts[0].time_window.from_time, datetime(day=1, month=5, year=2005, hour=4, minute=4, second=0))
        self.assertEqual(list_of_algorithm_conflicts[0].time_window.to_time, datetime(day=1, month=5, year=2005, hour=4, minute=7, second=0))

        self.assertIsInstance(list_of_algorithm_conflicts[0].involved_train_path_node_references, list)
        self.assertEqual(len(list_of_algorithm_conflicts[0].involved_train_path_node_references), 3)
        self.assertEqual(list_of_algorithm_conflicts[0].involved_train_path_node_references[0].train_id, 1234)
        self.assertEqual(list_of_algorithm_conflicts[0].involved_train_path_node_references[0].train_path_node_id, 12345)
        self.assertEqual(list_of_algorithm_conflicts[0].involved_train_path_node_references[1].train_id, 1235)
        self.assertEqual(list_of_algorithm_conflicts[0].involved_train_path_node_references[1].train_path_node_id, 12346)
        self.assertEqual(list_of_algorithm_conflicts[0].involved_train_path_node_references[2].train_id, 1236)
        self.assertEqual(list_of_algorithm_conflicts[0].involved_train_path_node_references[2].train_path_node_id, 12347)

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
