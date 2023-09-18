from datetime import datetime
import unittest
from unittest import mock

from py_client.aidm import AlgorithmTrainPathNodeReference
from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm.aidm_conflict import (
    ConflictDetectionArguments,
    AlgorithmNodeConflict,
    AlgorithmTwoTrainsConflict,
    _AlgorithmTwoTrainsNodeConflict,
    ConflictType,
    AlgorithmConflictDetectionEventType,
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
                "   { \n"
                '       "conflictType": "sameStationTrackSeparationTime", \n'
                '       "timeWindow": { \n'
                '           "fromTime": "2005-05-01T04:04:00", \n'
                '           "toTime": "2005-05-01T04:06:00" \n'
                "       }, \n"
                '       "nodeId": 352, \n'
                '       "causingTrainPathNode": { \n'
                '           "trainId": 1230, \n'
                '           "trainPathNodeId": 1228 \n'
                "       }, \n"
                '       "causingEventType": "departure", \n'
                '       "affectedTrainPathNode": { \n'
                '           "trainId": 1234, \n'
                '           "trainPathNodeId": 1232 \n'
                "       }, \n"
                '       "affectedEventType": "arrival" \n'
                "   }, \n"
                "   { \n"
                '       "conflictType": "sameSectionTrackSeparationTime", \n'
                '       "timeWindow": { \n'
                '           "fromTime": "2005-05-01T04:04:00", \n'
                '           "toTime": "2005-05-01T04:06:00" \n'
                "       }, \n"
                '       "nodeId": 352, \n'
                '       "affectedTrainPathNode": { \n'
                '           "trainId": 1226, \n'
                '           "trainPathNodeId": 1224 \n'
                "       }, \n"
                '       "affectedEventType": "arrival", \n'
                '       "causingTrainPathNode": { \n'
                '           "trainId": 1230, \n'
                '           "trainPathNodeId": 1228 \n'
                "       }, \n"
                '       "causingEventType": "departure" \n'
                "   }, \n"
                "   { \n"
                '       "conflictType": "incompatibleStationRoutes", \n'
                '       "timeWindow": { \n'
                '           "fromTime": "2005-05-01T04:15:00", \n'
                '           "toTime": "2005-05-01T04:16:00" \n'
                "       }, \n"
                '       "nodeId": 482, \n'
                '       "affectedTrainPathNode": { \n'
                '           "trainId": 1226, \n'
                '           "trainPathNodeId": 1246 \n'
                "       }, \n"
                '       "affectedEventType": "departure", \n'
                '       "causingTrainPathNode": { \n'
                '           "trainId": 1230, \n'
                '           "trainPathNodeId": 1275 \n'
                "       }, \n"
                '       "causingEventType": "arrival" \n'
                "   }, \n"
                "   { \n"
                '       "conflictType": "incompatibleJunctionRoutes", \n'
                '       "timeWindow": { \n'
                '           "fromTime": "2005-05-01T03:47:00", \n'
                '           "toTime": "2005-05-01T03:52:00" \n'
                "       }, \n"
                '       "nodeId": 7894, \n'
                '       "affectedTrainPathNode": { \n'
                '           "trainId": 1226, \n'
                '           "trainPathNodeId": 2285 \n'
                "       }, \n"
                '       "affectedEventType": "arrival", \n'
                '       "causingTrainPathNode": { \n'
                '           "trainId": 1230, \n'
                '           "trainPathNodeId": 9678 \n'
                "       }, \n"
                '       "causingEventType": "departure" \n'
                "   }, \n"
                "   { \n"
                '       "conflictType": "levelTrackCrossingTime", \n'
                '       "timeWindow": { \n'
                '           "fromTime": "2005-05-01T03:47:00", \n'
                '           "toTime": "2005-05-01T03:52:00" \n'
                "       }, \n"
                '       "nodeId": 7894, \n'
                '       "affectedTrainPathNode": { \n'
                '           "trainId": 1226, \n'
                '           "trainPathNodeId": 2285 \n'
                "       }, \n"
                '       "affectedEventType": "arrival", \n'
                '       "causingTrainPathNode": { \n'
                '           "trainId": 1230, \n'
                '           "trainPathNodeId": 9678 \n'
                "       }, \n"
                '       "causingEventType": "departure" \n'
                "   } \n"
                "]"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_mock_session(self, mocked_get_obj):
        train_ids = [1226, 1230, 1234]
        arguments = ConflictDetectionArguments(train_ids=train_ids).with_type_filter(
            [
                ConflictType.SameStationTrackSeparationTime,
                ConflictType.SameSectionTrackSeparationTime,
                ConflictType.IncompatibleStationRoutes,
                ConflictType.IncompatibleJunctionRoutes,
                ConflictType.LevelTrackCrossingTime,
            ]
        )

        self.interface_to_viriato.detect_conflicts(arguments=arguments)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._DetectConflictsMockSession__last_request, get_api_url() + "/services/trains:detect-conflicts")

        self.assertDictEqual(
            session_obj._DetectConflictsMockSession__last_body,
            {
                "trainIds": [1226, 1230, 1234],
                "filters": {
                    "location": {"nodeIds": None, "sectionTrackIds": None},
                    "conflictTypes": [
                        "sameStationTrackSeparationTime",
                        "sameSectionTrackSeparationTime",
                        "incompatibleStationRoutes",
                        "incompatibleJunctionRoutes",
                        "levelTrackCrossingTime",
                    ],
                },
            },
        )
        self.assertDictEqual(session_obj._DetectConflictsMockSession__last_params, {})

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_response(self, mocked_get_obj):
        arguments = ConflictDetectionArguments(train_ids=[1230, 1234])
        list_of_algorithm_conflicts = self.interface_to_viriato.detect_conflicts(arguments=arguments)

        self.assertIsInstance(list_of_algorithm_conflicts, list)

        self.assertIsInstance(list_of_algorithm_conflicts[0], AlgorithmNodeConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[0], AlgorithmTwoTrainsConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[0], _AlgorithmTwoTrainsNodeConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[0].conflict_type, ConflictType)
        self.assertEqual(list_of_algorithm_conflicts[0].conflict_type, ConflictType.SameStationTrackSeparationTime)
        self.assertIsInstance(list_of_algorithm_conflicts[0].time_window, TimeWindow)
        self.assertEqual(list_of_algorithm_conflicts[0].time_window.from_time, datetime(day=1, month=5, year=2005, hour=4, minute=4, second=0))
        self.assertEqual(list_of_algorithm_conflicts[0].time_window.to_time, datetime(day=1, month=5, year=2005, hour=4, minute=6, second=0))
        self.assertEqual(list_of_algorithm_conflicts[0].node_id, 352)

        causing_train_path_node = list_of_algorithm_conflicts[0].causing_train_path_node
        self.assertIsInstance(causing_train_path_node, AlgorithmTrainPathNodeReference)
        self.assertEqual(causing_train_path_node.train_path_node_id, 1228)
        self.assertEqual(causing_train_path_node.train_id, 1230)

        affected_train_path_node = list_of_algorithm_conflicts[0].affected_train_path_node
        self.assertIsInstance(affected_train_path_node, AlgorithmTrainPathNodeReference)
        self.assertEqual(affected_train_path_node.train_id, 1234)
        self.assertEqual(affected_train_path_node.train_path_node_id, 1232)
        self.assertIsInstance(list_of_algorithm_conflicts[0].affected_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[0].affected_event_type, AlgorithmConflictDetectionEventType.Arrival)
        self.assertIsInstance(list_of_algorithm_conflicts[0].causing_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[0].causing_event_type, AlgorithmConflictDetectionEventType.Departure)

        self.assertIsInstance(list_of_algorithm_conflicts[1], AlgorithmNodeConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[1], AlgorithmTwoTrainsConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[1], _AlgorithmTwoTrainsNodeConflict)
        self.assertEqual(list_of_algorithm_conflicts[1].conflict_type, ConflictType.SameSectionTrackSeparationTime)
        self.assertIsInstance(list_of_algorithm_conflicts[1].causing_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[1].causing_event_type, AlgorithmConflictDetectionEventType.Departure)
        self.assertIsInstance(list_of_algorithm_conflicts[1].affected_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[1].affected_event_type, AlgorithmConflictDetectionEventType.Arrival)

        self.assertIsInstance(list_of_algorithm_conflicts[2], AlgorithmNodeConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[2], AlgorithmTwoTrainsConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[2], _AlgorithmTwoTrainsNodeConflict)
        self.assertEqual(list_of_algorithm_conflicts[2].conflict_type, ConflictType.IncompatibleStationRoutes)
        self.assertIsInstance(list_of_algorithm_conflicts[2].causing_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[2].causing_event_type, AlgorithmConflictDetectionEventType.Arrival)
        self.assertIsInstance(list_of_algorithm_conflicts[2].affected_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[2].affected_event_type, AlgorithmConflictDetectionEventType.Departure)

        self.assertIsInstance(list_of_algorithm_conflicts[3], AlgorithmNodeConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[3], AlgorithmTwoTrainsConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[3], _AlgorithmTwoTrainsNodeConflict)
        self.assertEqual(list_of_algorithm_conflicts[3].conflict_type, ConflictType.IncompatibleJunctionRoutes)
        self.assertIsInstance(list_of_algorithm_conflicts[3].causing_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[3].causing_event_type, AlgorithmConflictDetectionEventType.Departure)
        self.assertIsInstance(list_of_algorithm_conflicts[3].affected_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[3].affected_event_type, AlgorithmConflictDetectionEventType.Arrival)

        self.assertIsInstance(list_of_algorithm_conflicts[4], AlgorithmNodeConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[4], AlgorithmTwoTrainsConflict)
        self.assertIsInstance(list_of_algorithm_conflicts[4], _AlgorithmTwoTrainsNodeConflict)
        self.assertEqual(list_of_algorithm_conflicts[4].conflict_type, ConflictType.LevelTrackCrossingTime)
        self.assertIsInstance(list_of_algorithm_conflicts[4].causing_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[4].causing_event_type, AlgorithmConflictDetectionEventType.Departure)
        self.assertIsInstance(list_of_algorithm_conflicts[4].affected_event_type, AlgorithmConflictDetectionEventType)
        self.assertEqual(list_of_algorithm_conflicts[4].affected_event_type, AlgorithmConflictDetectionEventType.Arrival)

    @mock.patch("requests.Session", side_effect=DetectConflictsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
