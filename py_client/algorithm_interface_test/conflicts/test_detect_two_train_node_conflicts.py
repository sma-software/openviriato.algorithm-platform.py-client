import datetime
import unittest
from unittest import mock
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm.aidm_conflict import ConflictDetectionArguments, _AlgorithmNodeConflict, _AlgorithmTwoTrainConflict, AlgorithmTwoTrainNodeConflict, ConflictType
from py_client.aidm.aidm_time_window_classes import TimeWindow

class TestDetectConflicts(unittest.TestCase):
    class DetectConflictsMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = ( "["
                            "   { \n"
                            "       \"conflictType\": \"sameStationTrack\", \n"
                            "       \"timeWindow\": { \n"
                            "           \"fromTime\": \"2005-05-01T04:04:00\", \n"
                            "           \"toTime\": \"2005-05-01T04:06:00\" \n"
                            "       }, \n"
                            "       \"nodeId\": 352, \n"
                            "       \"precedingTrainId\": 1230, \n"
                            "       \"precedingTrainPathNodeId\": 1228, \n"
                            "       \"succeedingTrainId\": 1234, \n"
                            "       \"succeedingTrainPathNodeId\": 1232 \n"
                            "   }, \n"
                            "   { \n"
                            "       \"conflictType\": \"sameSectionTrack\", \n"
                            "       \"timeWindow\": { \n"
                            "           \"fromTime\": \"2005-05-01T04:04:00\", \n"
                            "           \"toTime\": \"2005-05-01T04:06:00\" \n"
                            "       }, \n"
                            "       \"nodeId\": 352, \n"
                            "       \"precedingTrainId\": 1226, \n"
                            "       \"precedingTrainPathNodeId\": 1224, \n"
                            "       \"succeedingTrainId\": 1230, \n"
                            "       \"succeedingTrainPathNodeId\": 1228 \n"
                            "   }, \n"
                            "   { \n"
                            "       \"conflictType\": \"incompatibleStationRoutes\", \n"
                            "       \"timeWindow\": { \n"
                            "           \"fromTime\": \"2005-05-01T04:15:00\", \n"
                            "           \"toTime\": \"2005-05-01T04:16:00\" \n"
                            "       }, \n"
                            "       \"nodeId\": 482, \n"
                            "       \"precedingTrainId\": 1226, \n"
                            "       \"precedingTrainPathNodeId\": 1246, \n"
                            "       \"succeedingTrainId\": 1230, \n"
                            "       \"succeedingTrainPathNodeId\": 1275 \n"
                            "   }, \n"
                            "   { \n"
                            "       \"conflictType\": \"incompatibleJunctionRoutes\", \n"
                            "       \"timeWindow\": { \n"
                            "           \"fromTime\": \"2005-05-01T03:47:00\", \n"
                            "           \"toTime\": \"2005-05-01T03:52:00\" \n"
                            "       }, \n"
                            "       \"nodeId\": 7894, \n"
                            "       \"precedingTrainId\": 1226, \n"
                            "       \"precedingTrainPathNodeId\": 2285, \n"
                            "       \"succeedingTrainId\": 1230, \n"
                            "       \"succeedingTrainPathNodeId\": 9678 \n"
                            "   } \n"
                            "]"
                            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_mock_session(self, mocked_get_obj):
        train_ids = [1226, 1230, 1234]
        arguments = ConflictDetectionArguments(train_ids = train_ids)

        self.interface_to_viriato.detect_conflicts(arguments = arguments)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._DetectConflictsMockSession__last_request,
                         get_api_url() + "/services/trains:detect-conflicts")

        self.assertDictEqual(session_obj._DetectConflictsMockSession__last_body, {'trainIds': [1226, 1230, 1234]})

    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def test_detect_conflicts_response(self, mocked_get_obj):
        arguments = ConflictDetectionArguments(train_ids = [1230, 1234])
        list_of_algorithm_conflicts = self.interface_to_viriato.detect_conflicts(arguments = arguments)

        self.assertIsInstance(
            list_of_algorithm_conflicts,
            list)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0],
            _AlgorithmNodeConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0],
            _AlgorithmTwoTrainConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0],
            AlgorithmTwoTrainNodeConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0].conflict_type,
            ConflictType)

        self.assertEqual(
            list_of_algorithm_conflicts[0].conflict_type,
            ConflictType.SameStationTrack)

        self.assertIsInstance(
            list_of_algorithm_conflicts[0].time_window,
            TimeWindow)

        self.assertEqual(
            list_of_algorithm_conflicts[0].time_window.from_time,
            datetime.datetime(day=1, month=5, year=2005, hour=4, minute=4, second=0))

        self.assertEqual(
            list_of_algorithm_conflicts[0].time_window.to_time,
            datetime.datetime(day=1, month=5, year=2005, hour=4, minute=6, second=0))

        self.assertEqual(
            list_of_algorithm_conflicts[0].node_id,
            352)

        self.assertEqual(
            list_of_algorithm_conflicts[0].preceding_train_id,
            1230)

        self.assertEqual(
            list_of_algorithm_conflicts[0].preceding_train_path_node_id,
            1228)

        self.assertEqual(
            list_of_algorithm_conflicts[0].succeeding_train_id,
            1234)

        self.assertEqual(
            list_of_algorithm_conflicts[0].succeeding_train_path_node_id,
            1232)



        self.assertIsInstance(
            list_of_algorithm_conflicts[1],
            _AlgorithmNodeConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[1],
            _AlgorithmTwoTrainConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[1],
            AlgorithmTwoTrainNodeConflict)

        self.assertEqual(
            list_of_algorithm_conflicts[1].conflict_type,
            ConflictType.SameSectionTrack)

        self.assertIsInstance(
            list_of_algorithm_conflicts[2],
            _AlgorithmNodeConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[2],
            _AlgorithmTwoTrainConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[2],
            AlgorithmTwoTrainNodeConflict)

        self.assertEqual(
            list_of_algorithm_conflicts[2].conflict_type,
            ConflictType.IncompatibleStationRoutes)

        self.assertIsInstance(
            list_of_algorithm_conflicts[3],
            _AlgorithmNodeConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[3],
            _AlgorithmTwoTrainConflict)

        self.assertIsInstance(
            list_of_algorithm_conflicts[3],
            AlgorithmTwoTrainNodeConflict)

        self.assertEqual(
            list_of_algorithm_conflicts[3].conflict_type,
            ConflictType.IncompatibleJunctionRoutes)





    @mock.patch('requests.Session', side_effect=DetectConflictsMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)