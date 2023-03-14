from datetime import datetime, timedelta
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import UpdateStopTimesTrainPathNode, AlgorithmTrain, AlgorithmTrainPathNode, StopStatus, UpdateRunTimesTrainPathSegment
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestUpdateTrajectory(unittest.TestCase):
    class UpdateTrajectoryTestMockSession(SessionMockTestBase):
        def put(self, request, json):
            self._last_body = json
            self._last_request = request
            json_string = (
                "{ \n"
                '  "id": 2060,\n'
                '  "code": "TestUpdateTrajectory",'
                '  "trainPathNodes": [\n'
                "    {\n"
                '      "id": 1332,\n'
                '      "sectionTrackId": null,\n'
                '      "nodeId": 18,\n'
                '      "nodeTrackId": null,\n'
                '      "FormationId": 1187,\n'
                '      "movementTypeId": null,\n'
                '      "arrivalTime": "2003-05-01T00:04:00",\n'
                '      "departureTime": "2003-05-01T00:05:30",\n'
                '      "minimumRunTime": null,\n'
                '      "minimumStopTime": "P0D",\n'
                '      "stopStatus": "operationalStop",\n'
                '      "sequenceNumber": 0\n'
                "    },\n"
                "    {\n"
                '      "id": 1696,\n'
                '      "sectionTrackId": 1172,\n'
                '      "nodeId": 10,\n'
                '      "nodeTrackId": null,\n'
                '      "FormationId": null,\n'
                '      "movementTypeId": null,\n'
                '      "arrivalTime": "2003-05-01T00:10:30",\n'
                '      "departureTime": "2003-05-01T00:10:30",\n'
                '      "minimumRunTime": "PT5M",\n'
                '      "minimumStopTime": "P0D",\n'
                '      "stopStatus": "commercialStop",\n'
                '      "sequenceNumber": 1\n'
                "    }\n"
                "  ],\n"
                '  "debugString": "Mocked RVZH_1_1_J03 tt_(G)"\n'
                "}"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=UpdateTrajectoryTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=UpdateTrajectoryTestMockSession)
    def test_update_trajectory_request(self, mocked_get_obj):
        train_id = 2060
        update_train_stop_time_node = UpdateStopTimesTrainPathNode(
            train_path_node_id=1332,
            arrival_time=datetime(2003, 5, 1, 0, 4),
            departure_time=datetime(2003, 5, 1, 0, 5),
            stop_status=StopStatus.operational_stop,
            minimum_stop_time=timedelta(seconds=30),
        )

        self.interface_to_viriato.update_train_trajectory_stop_times(train_id, update_train_stop_time_node)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/trains/2060/train-path-nodes:update-trajectory-stop-times")
        self.assertDictEqual(
            session_obj.last_body,
            dict(
                trainPathNodeId=1332,
                arrivalTime="2003-05-01T00:04:00",
                departureTime="2003-05-01T00:05:00",
                minimumStopTime="PT30S",
                stopStatus="operationalStop",
            ),
        )

    @mock.patch("requests.Session", side_effect=UpdateTrajectoryTestMockSession)
    def test_update_trajectory_response(self, mocked_get_obj):
        train_id = 2060
        update_train_stop_time_node = UpdateStopTimesTrainPathNode(
            train_path_node_id=1332,
            arrival_time=datetime(2003, 5, 1, 0, 4),
            departure_time=datetime(2003, 5, 1, 0, 5),
            stop_status=StopStatus.operational_stop,
            minimum_stop_time=timedelta(seconds=30),
        )

        updated_algorithm_train = self.interface_to_viriato.update_train_trajectory_stop_times(train_id, update_train_stop_time_node)

        self.assertIsInstance(updated_algorithm_train, AlgorithmTrain)
        self.assertEqual(updated_algorithm_train.debug_string, "Mocked RVZH_1_1_J03 tt_(G)")
        self.assertEqual(updated_algorithm_train.code, "TestUpdateTrajectory")
        self.assertEqual(updated_algorithm_train.id, 2060)
        self.assertIsInstance(updated_algorithm_train.train_path_nodes, list)
        self.assertIsInstance(updated_algorithm_train.train_path_nodes[0], AlgorithmTrainPathNode)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].id, 1332)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].section_track_id, None)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].node_track_id, None)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].formation_id, 1187)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].arrival_time, datetime(2003, 5, 1, 0, 4))
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].departure_time, datetime(2003, 5, 1, 0, 5, 30))
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].minimum_run_time, None)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].minimum_stop_time, timedelta(0))
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].stop_status, StopStatus.operational_stop)

    @mock.patch("requests.Session", side_effect=UpdateTrajectoryTestMockSession)
    def test_update_trajectory_request_with_update_train_path_segment(self, mocked_get_obj):
        train_id = 20610
        update_train_path_segment = UpdateRunTimesTrainPathSegment(
            to_train_path_node_id=1332,
            to_node_arrival_time=datetime(2003, 5, 1, 0, 4),
            from_node_departure_time=datetime(2003, 5, 1, 0, 5),
            minimum_run_time=timedelta(seconds=120),
        )

        self.interface_to_viriato.update_train_trajectory_run_times(train_id, update_train_path_segment)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/trains/20610/train-path-nodes:update-trajectory-run-times")
        self.assertDictEqual(
            session_obj.last_body,
            dict(toTrainPathNodeId=1332, toNodeArrivalTime="2003-05-01T00:04:00", fromNodeDepartureTime="2003-05-01T00:05:00", minimumRunTime="PT2M"),
        )

    @mock.patch("requests.Session", side_effect=UpdateTrajectoryTestMockSession)
    def test_update_trajectory_request_with_update_train_path_segment_minimum_run_time_none(self, mocked_get_obj):
        train_id = 2062
        update_train_path_segment = UpdateRunTimesTrainPathSegment(
            to_train_path_node_id=1332,
            to_node_arrival_time=datetime(2003, 5, 1, 0, 4),
            from_node_departure_time=datetime(2003, 5, 1, 0, 5),
            minimum_run_time=None,
        )

        self.interface_to_viriato.update_train_trajectory_run_times(train_id, update_train_path_segment)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/trains/2062/train-path-nodes:update-trajectory-run-times")
        self.assertDictEqual(
            session_obj.last_body,
            dict(toTrainPathNodeId=1332, toNodeArrivalTime="2003-05-01T00:04:00", fromNodeDepartureTime="2003-05-01T00:05:00", minimumRunTime=None),
        )

    @mock.patch("requests.Session", side_effect=UpdateTrajectoryTestMockSession)
    def test_update_trajectory_response_with_update_train_path_segment(self, mocked_get_obj):
        train_id = 2060
        update_train_path_segment = UpdateRunTimesTrainPathSegment(
            to_train_path_node_id=1332,
            to_node_arrival_time=datetime(2003, 5, 1, 0, 4),
            from_node_departure_time=datetime(2003, 5, 1, 0, 5),
            minimum_run_time=None,
        )

        updated_algorithm_train = self.interface_to_viriato.update_train_trajectory_run_times(train_id, update_train_path_segment)

        self.assertIsInstance(updated_algorithm_train, AlgorithmTrain)
        self.assertEqual(updated_algorithm_train.debug_string, "Mocked RVZH_1_1_J03 tt_(G)")
        self.assertEqual(updated_algorithm_train.code, "TestUpdateTrajectory")
        self.assertEqual(updated_algorithm_train.id, 2060)
        self.assertIsInstance(updated_algorithm_train.train_path_nodes, list)
        self.assertIsInstance(updated_algorithm_train.train_path_nodes[0], AlgorithmTrainPathNode)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].id, 1332)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].section_track_id, None)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].node_track_id, None)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].formation_id, 1187)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].arrival_time, datetime(2003, 5, 1, 0, 4))
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].departure_time, datetime(2003, 5, 1, 0, 5, 30))
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].minimum_run_time, None)
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].minimum_stop_time, timedelta(0))
        self.assertEqual(updated_algorithm_train.train_path_nodes[0].stop_status, StopStatus.operational_stop)

    @mock.patch("requests.Session", side_effect=UpdateTrajectoryTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
