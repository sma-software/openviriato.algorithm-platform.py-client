import unittest
from unittest import mock

import AIDMClasses
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestRerouteTrain(unittest.TestCase):
    class RerouteTrainTestMockSession(SessionMockTestBase):
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = (
                "             {\n"
                "                    \"ID\": 3516,\n"
                "                    \"TrainPathNodes\": [\n"
                "                        {\n"
                "                            \"ID\": 2424,\n"
                "                            \"SectionTrackID\": null,\n"
                "                            \"NodeID\": 7,\n"
                "                            \"NodeTrackID\": 8,\n"
                "                            \"FormationID\": 1187,\n"
                "                            \"ArrivalTime\": \"2003-05-01T00:10:00\",\n"
                "                            \"DepartureTime\": \"2003-05-01T00:10:00\",\n"
                "                            \"MinimumRunTime\": null,\n"
                "                            \"MinimumStopTime\": \"P0D\",\n"
                "                            \"StopStatus\": \"commercialStop\",\n"
                "                            \"SequenceNumber\": 0\n"
                "                        },\n"
                "                        {\n"
                "                            \"ID\": 11040,\n"
                "                            \"SectionTrackID\": 1165,\n"
                "                            \"NodeID\": 24,\n"
                "                            \"NodeTrackID\": 25,\n"
                "                            \"FormationID\": 1187,\n"
                "                            \"ArrivalTime\": \"2003-05-01T00:10:00\",\n"
                "                            \"DepartureTime\": \"2003-05-01T00:10:00\",\n"
                "                            \"MinimumRunTime\": \"P0D\",\n"
                "                            \"MinimumStopTime\": \"P0D\",\n"
                "                            \"StopStatus\": \"passing\",\n"
                "                            \"SequenceNumber\": 1\n"
                "                        },\n"
                "                        {\n"
                "                            \"ID\": 3152,\n"
                "                            \"SectionTrackID\": 1166,\n"
                "                            \"NodeID\": 10,\n"
                "                            \"NodeTrackID\": 12,\n"
                "                            \"FormationID\": null,\n"
                "                            \"ArrivalTime\": \"2003-05-01T00:19:00\",\n"
                "                            \"DepartureTime\": \"2003-05-01T00:19:00\",\n"
                "                            \"MinimumRunTime\": \"PT9M\",\n"
                "                            \"MinimumStopTime\": \"P0D\",\n"
                "                            \"StopStatus\": \"commercialStop\",\n"
                "                            \"SequenceNumber\": 2\n"
                "                        }\n"
                "                    ],\n"
                "                    \"DebugString\": \"RVZH_3_1_J03 tt_(S)\"\n"
                "                }")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def setUp(self, mocked_session):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def test_reroute_train_request(self, mocked_session):
        train_id = 2060
        start_train_path_node_id = 2424
        end_train_path_node_id = 3152
        routing_edges = [AIDMClasses.OutgoingRoutingEdge(NodeID=7, StartNodeTrackID=8, EndSectionTrackID=1165),
                         AIDMClasses.IncomingRoutingEdge(NodeID=24, StartSectionTrackID=1165, EndNodeTrackID=25),
                         AIDMClasses.OutgoingRoutingEdge(NodeID=24, StartNodeTrackID=25, EndSectionTrackID=1166),
                         AIDMClasses.IncomingRoutingEdge(NodeID=10, StartSectionTrackID=1166, EndNodeTrackID=12)]

        test_route = AIDMClasses.AIDM_Update_classes.UpdateTrainRoute(TrainID=train_id,
                                                                      EndTrainPathNodeID=end_train_path_node_id,
                                                                      StartTrainPathNodeID=start_train_path_node_id,
                                                                      RoutingEdges=routing_edges)

        self.interface_to_viriato.reroute_train(test_route)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        expected_routing_edge_body = [dict(NodeID=7, StartNodeTrackID=8, EndSectionTrackID=1165),
                                      dict(NodeID=24, StartSectionTrackID=1165, EndNodeTrackID=25),
                                      dict(NodeID=24, StartNodeTrackID=25, EndSectionTrackID=1166),
                                      dict(NodeID=10, StartSectionTrackID=1166, EndNodeTrackID=12)]

        self.assertEqual(get_api_url() + "/reroute-train",
                         session_obj._RerouteTrainTestMockSession__last_request)
        self.assertListEqual(session_obj._RerouteTrainTestMockSession__last_body['RoutingEdges'],
                             expected_routing_edge_body)
        self.assertDictEqual(session_obj._RerouteTrainTestMockSession__last_body["RoutingEdges"][0],
                             expected_routing_edge_body[0])
        self.assertEqual(session_obj._RerouteTrainTestMockSession__last_body["StartTrainPathNodeID"], 2424)
        self.assertEqual(session_obj._RerouteTrainTestMockSession__last_body["EndTrainPathNodeID"], 3152)

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def test_reroute_train_response(self, mocked_session):
        train_id = 2060
        start_train_path_node_id = 2424
        end_train_path_node_id = 3152
        routing_edges = [AIDMClasses.OutgoingRoutingEdge(NodeID=7, StartNodeTrackID=8, EndSectionTrackID=1165),
                         AIDMClasses.IncomingRoutingEdge(NodeID=24, StartSectionTrackID=1165, EndNodeTrackID=25),
                         AIDMClasses.OutgoingRoutingEdge(NodeID=24, StartNodeTrackID=25, EndSectionTrackID=1166),
                         AIDMClasses.IncomingRoutingEdge(NodeID=10, StartSectionTrackID=1166, EndNodeTrackID=12)]

        test_route = AIDMClasses.AIDM_Update_classes.UpdateTrainRoute(TrainID=train_id,
                                                                      EndTrainPathNodeID=end_train_path_node_id,
                                                                      StartTrainPathNodeID=start_train_path_node_id,
                                                                      RoutingEdges=routing_edges)

        rerouted_algorithm_train = self.interface_to_viriato.reroute_train(test_route)

        self.assertEqual(rerouted_algorithm_train.ID, 3516)
        self.assertEqual(rerouted_algorithm_train.DebugString, "RVZH_3_1_J03 tt_(S)")
        self.assertIsInstance(rerouted_algorithm_train.TrainPathNodes, list)
        self.assertIsInstance(rerouted_algorithm_train.TrainPathNodes[0], AIDMClasses.TrainPathNode)
        self.assertEqual(rerouted_algorithm_train.TrainPathNodes[0].ID, 2424)

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def tearDown(self, mocked_session) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
