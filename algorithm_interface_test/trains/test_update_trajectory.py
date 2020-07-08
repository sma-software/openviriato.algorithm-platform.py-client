import datetime
import unittest
from unittest import mock
from aidm import UpdateTrainStopTimesNode, AlgorithmTrain, AlgorithmTrainPathNode, StopStatus
from algorithm_interface.algorithm_interface import AlgorithmInterface
import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestUpdateTrajectory(unittest.TestCase):
    class UpdateTrajectoryTestMockSession(SessionMockTestBase):
        def put(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = ("{ \n"
                           "  \"ID\": 2060,\n"
                           "  \"TrainPathNodes\": [\n"
                           "    {\n"
                           "      \"ID\": 1332,\n"
                           "      \"SectionTrackID\": null,\n"
                           "      \"node_id\": 18,\n"
                           "      \"node_track_id\": null,\n"
                           "      \"FormationID\": 1187,\n"
                           "      \"ArrivalTime\": \"2003-05-01T00:04:00\",\n"
                           "      \"DepartureTime\": \"2003-05-01T00:05:30\",\n"
                           "      \"MinimumRunTime\": null,\n"
                           "      \"MinimumStopTime\": \"P0D\",\n"
                           "      \"StopStatus\": \"operationalStop\",\n"
                           "      \"SequenceNumber\": 0\n"
                           "    },\n"
                           "    {\n"
                           "      \"ID\": 1696,\n"
                           "      \"SectionTrackID\": 1172,\n"
                           "      \"node_id\": 10,\n"
                           "      \"node_track_id\": null,\n"
                           "      \"FormationID\": null,\n"
                           "      \"ArrivalTime\": \"2003-05-01T00:10:30\",\n"
                           "      \"DepartureTime\": \"2003-05-01T00:10:30\",\n"
                           "      \"MinimumRunTime\": \"PT5M\",\n"
                           "      \"MinimumStopTime\": \"P0D\",\n"
                           "      \"StopStatus\": \"commercialStop\",\n"
                           "      \"SequenceNumber\": 1\n"
                           "    }\n"
                           "  ],\n"
                           "  \"DebugString\": \"Mocked RVZH_1_1_J03 tt_(G)\"\n"
                           "}")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=UpdateTrajectoryTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=UpdateTrajectoryTestMockSession)
    def test_update_trajectory_request(self, mocked_get_obj):
        train_id = 2060
        update_train_stop_time_node = UpdateTrainStopTimesNode(train_path_node_id=1332,
                                                               arrival_time=datetime.datetime(2003, 5, 1, 0, 4),
                                                               departure_time=datetime.datetime(2003, 5, 1, 0, 5),
                                                               stop_status=StopStatus.operational_stop,
                                                               minimum_stop_time=datetime.timedelta(seconds=30))

        self.interface_to_viriato.update_trajectory(train_id, update_train_stop_time_node)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._UpdateTrajectoryTestMockSession__last_request,
                         get_api_url() + '/trains/2060/train-path-nodes:update-trajectory-stop-times')
        self.assertDictEqual(session_obj._UpdateTrajectoryTestMockSession__last_body,
                             dict(TrainPathNodeID=1332,
                                  ArrivalTime="2003-05-01T00:04:00",
                                  DepartureTime="2003-05-01T00:05:00",
                                  MinimumStopTime="PT30S",
                                  StopStatus="OperationalStop"))

    @mock.patch('requests.Session', side_effect=UpdateTrajectoryTestMockSession)
    def test_update_trajectory_response(self, mocked_get_obj):
        train_id = 2060
        update_train_stop_time_node = UpdateTrainStopTimesNode(train_path_node_id=1332,
                                                               arrival_time=datetime.datetime(2003, 5, 1, 0, 4),
                                                               departure_time=datetime.datetime(2003, 5, 1, 0, 5),
                                                               stop_status=StopStatus.operational_stop,
                                                               minimum_stop_time=datetime.timedelta(seconds=30))

        updated_algorithm_train = self.interface_to_viriato.update_trajectory(train_id, update_train_stop_time_node)

        self.assertIsInstance(updated_algorithm_train, AlgorithmTrain)
        self.assertEqual(updated_algorithm_train.debug_string, 'Mocked RVZH_1_1_J03 tt_(G)')
        self.assertEqual(updated_algorithm_train.id, 2060)
        self.assertIsInstance(updated_algorithm_train.train_path_nodes, list)
        self.assertIsInstance(updated_algorithm_train.train_path_nodes[0], AlgorithmTrainPathNode)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].id, 1332)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].section_track_id, None)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].node_track_id, None)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].formation_id, 1187)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].arrival_time, datetime.datetime(2003, 5, 1, 0, 4))
        self.assertEqual(
            updated_algorithm_train.train_path_nodes[0].departure_time,
            datetime.datetime(2003, 5, 1, 0, 5, 30))
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].minimum_run_time, None)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].minimum_stop_time, datetime.timedelta(0))
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].stop_status, StopStatus.operational_stop)

    @mock.patch('requests.Session', side_effect=UpdateTrajectoryTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
