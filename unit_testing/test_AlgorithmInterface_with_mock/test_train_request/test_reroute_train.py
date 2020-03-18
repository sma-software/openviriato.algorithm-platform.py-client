import datetime
import unittest
from unittest import mock

import AIDMClasses.AIDM_classes as AIDM_classes
import AlgorithmInterface.AlgorithmInterface
import unit_testing.test_AlgorithmInterface_with_mock.unit_testing_requisites.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_requisites.unit_testing_with_mock_helpers import \
    get_api_url, SessionMockTestBase


class TestRerouteTrain(unittest.TestCase):
    class RerouteTrainTestMockSession(SessionMockTestBase):
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = ("{\n"
                           "  \"ID\": 3516,\n"
                           "  \"TrainPathNodes\": [\n"
                           "    {\n"
                           "      \"ID\": 2424,\n"
                           "      \"SectionTrackID\": null,\n"
                           "      \"NodeID\": 7,\n"
                           "      \"NodeTrackID\": 8,\n"
                           "      \"FormationID\": 1187,\n"
                           "      \"ArrivalTime\": \"2003-05-01T00:10:00\",\n"
                           "      \"DepartureTime\": \"2003-05-01T00:10:00\",\n"
                           "      \"MinimumRunTime\": null,\n"
                           "      \"MinimumStopTime\": \"P0D\",\n"
                           "      \"StopStatus\": \"commercialStop\",\n"
                           "      \"SequenceNumber\": 0\n"
                           "    },\n"
                           "    {\n"
                           "      \"ID\": 11040,\n"
                           "      \"SectionTrackID\": 1165,\n"
                           "      \"NodeID\": 24,\n"
                           "      \"NodeTrackID\": 25,\n"
                           "      \"FormationID\": 1187,\n"
                           "      \"ArrivalTime\": \"2003-05-01T00:10:00\",\n"
                           "      \"DepartureTime\": \"2003-05-01T00:10:00\",\n"
                           "      \"MinimumRunTime\": \"P0D\",\n"
                           "      \"MinimumStopTime\": \"P0D\",\n"
                           "      \"StopStatus\": \"passing\",\n"
                           "      \"SequenceNumber\": 1\n"
                           "    },\n"
                           "    {\n"
                           "      \"ID\": 3152,\n"
                           "      \"SectionTrackID\": 1166,\n"
                           "      \"NodeID\": 10,\n"
                           "      \"NodeTrackID\": 12,\n"
                           "      \"FormationID\": null,\n"
                           "      \"ArrivalTime\": \"2003-05-01T00:19:00\",\n"
                           "      \"DepartureTime\": \"2003-05-01T00:19:00\",\n"
                           "      \"MinimumRunTime\": \"PT9M\",\n"
                           "      \"MinimumStopTime\": \"P0D\",\n"
                           "      \"StopStatus\": \"commercialStop\",\n"
                           "      \"SequenceNumber\": 2\n"
                           "    }\n"
                           "  ],\n"
                           "  \"DebugString\": \"RVZH_3_1_J03 tt_(S)\"\n"
                           "}")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def setUp(self, mocked_session):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def test_reroute_train_request(self, mocked_session):
        train_id = 2060
        start_train_path_node_id = 2424
        end_train_path_node_id = 3152
        routing_edges = [AIDM_classes.OutgoingRoutingEdge(NodeID=7, StartNodeTrackID=8, EndSectionTrackID=1165),
                         AIDM_classes.IncomingRoutingEdge(NodeID=7, StartSectionTrackID=1165, EndNodeTrackID=25),
                         AIDM_classes.OutgoingRoutingEdge(NodeID=24, StartNodeTrackID=1166, EndSectionTrackID=1166),
                         AIDM_classes.IncomingRoutingEdge(NodeID=10, StartSectionTrackID=1166, EndNodeTrackID=12)]
        test_route = AIDM_classes.UpdateTrainRoute(TrainID=train_id, EndTrainPathNodeID=end_train_path_node_id,
                                                   StartTrainPathNodeID=start_train_path_node_id,
                                                   RoutingEdges=routing_edges)

        self.interface_to_viriato.reroute_train(test_route)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        expected_body = dict(TrainID=3516, StartTrainPathNodeId=2424, EndTrainPathNodeId=3152, RoutingEdges=[
            dict(nodeId=7, startNodeTrack=8, endSectionTrack=1165),
            dict(nodeId=24, startSectionTrack=1165, endNodeTrack=25),
            dict(nodeId=24, startNodeTrack=25, endSectionTrack=1166),
            dict(nodeId=10, startSectionTrack=1166, endNodeTrack=12)])
        self.maxDiff = None
        self.assertEqual(session_obj._RerouteTrainTestMockSession__last_request, get_api_url() + '/reroute-train')
        self.assertDictEqual(session_obj._RerouteTrainTestMockSession__last_body, expected_body)
        self.assertListEqual(session_obj._RerouteTrainTestMockSession__last_body['RoutingEdges'],
                             expected_body['RoutingEdges'])

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def test_reroute_train_response(self, mocked_session):
        train_id = 2060
        start_train_path_node_id = 2424
        end_train_path_node_id = 3152
        routing_edges = [AIDM_classes.OutgoingRoutingEdge(NodeID=7, StartNodeTrackID=8, EndSectionTrackID=1165),
                         AIDM_classes.IncomingRoutingEdge(NodeID=7, StartSectionTrackID=1165, EndNodeTrackID=25),
                         AIDM_classes.OutgoingRoutingEdge(NodeID=24, StartNodeTrackID=1166, EndSectionTrackID=1166),
                         AIDM_classes.IncomingRoutingEdge(NodeID=10, StartSectionTrackID=1166, EndNodeTrackID=12)]
        test_route = AIDM_classes.UpdateTrainRoute(TrainID=train_id, EndTrainPathNodeID=end_train_path_node_id,
                                                   StartTrainPathNodeID=start_train_path_node_id,
                                                   RoutingEdges=routing_edges)

        rerouted_algorithm_train = self.interface_to_viriato.reroute_train(test_route)

        self.assertEqual(rerouted_algorithm_train.ID, 3516)
        self.assertEqual(rerouted_algorithm_train.DebugString, "RVZH_3_1_J03 tt_(S)")
        self.assertIsInstance(rerouted_algorithm_train.TrainPathNodes, list)
        self.assertIsInstance(rerouted_algorithm_train.TrainPathNodes[0], AIDM_classes.TrainPathNode)
        self.assertEqual(rerouted_algorithm_train.TrainPathNodes[0].ID, 2424)

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def tearDown(self, mocked_session) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
