import unittest
from unittest import mock

from py_client.aidm import AlgorithmTrainPathNode, IncomingRoutingEdge, OutgoingRoutingEdge, UpdateTrainRoute
import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


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
                "                            \"node_id\": 7,\n"
                "                            \"node_track_id\": 8,\n"
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
                "                            \"node_id\": 24,\n"
                "                            \"node_track_id\": 25,\n"
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
                "                            \"node_id\": 10,\n"
                "                            \"node_track_id\": 12,\n"
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
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def test_reroute_train_request(self, mocked_session):
        train_id = 2060
        start_train_path_node_id = 2424
        end_train_path_node_id = 3152
        routing_edges = [OutgoingRoutingEdge(node_id=7, start_node_track_id=8, end_section_track_id=1165),
                         IncomingRoutingEdge(node_id=24, start_section_track_id=1165, end_node_track_id=25),
                         OutgoingRoutingEdge(node_id=24, start_node_track_id=25, end_section_track_id=1166),
                         IncomingRoutingEdge(node_id=10, start_section_track_id=1166, end_node_track_id=12)]

        test_route = UpdateTrainRoute(train_id=train_id,
                                      end_train_path_node_id=end_train_path_node_id,
                                      start_train_path_node_id=start_train_path_node_id,
                                      routing_edges=routing_edges)

        self.interface_to_viriato.reroute_train(test_route)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
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
        routing_edges = [OutgoingRoutingEdge(node_id=7, start_node_track_id=8, end_section_track_id=1165),
                         IncomingRoutingEdge(node_id=24, start_section_track_id=1165, end_node_track_id=25),
                         OutgoingRoutingEdge(node_id=24, start_node_track_id=25, end_section_track_id=1166),
                         IncomingRoutingEdge(node_id=10, start_section_track_id=1166, end_node_track_id=12)]

        test_route = UpdateTrainRoute(train_id=train_id,
                                      end_train_path_node_id=end_train_path_node_id,
                                      start_train_path_node_id=start_train_path_node_id,
                                      routing_edges=routing_edges)

        rerouted_algorithm_train = self.interface_to_viriato.reroute_train(test_route)

        self.assertEqual(rerouted_algorithm_train.id, 3516)
        self.assertEqual(rerouted_algorithm_train.debug_string, "RVZH_3_1_J03 tt_(S)")
        self.assertIsInstance(rerouted_algorithm_train.train_path_nodes, list)
        self.assertIsInstance(rerouted_algorithm_train.train_path_nodes[0], AlgorithmTrainPathNode)
        self.assertEqual(rerouted_algorithm_train.train_path_nodes[0].id, 2424)

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def tearDown(self, mocked_session) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
