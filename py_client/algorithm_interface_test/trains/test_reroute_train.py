import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import AlgorithmTrainPathNode, IncomingRoutingEdge, OutgoingRoutingEdge, UpdateTrainRoute
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestRerouteTrain(unittest.TestCase):
    class RerouteTrainTestMockSession(SessionMockTestBase):
        def put(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = (
                "             {\n"
                "                    \"id\": 3516,\n"
                "                    \"code\": \"TestRerouteTrain\",\n"
                "                    \"trainPathNodes\": [\n"
                "                        {\n"
                "                            \"id\": 2424,\n"
                "                            \"sectionTrackId\": null,\n"
                "                            \"nodeId\": 7,\n"
                "                            \"nodeTrackId\": 8,\n"
                "                            \"formationId\": 1187,\n"
                "                            \"arrivalTime\": \"2003-05-01T00:10:00\",\n"
                "                            \"departureTime\": \"2003-05-01T00:10:00\",\n"
                "                            \"minimumRunTime\": null,\n"
                "                            \"minimumStopTime\": \"P0D\",\n"
                "                            \"stopStatus\": \"commercialStop\",\n"
                "                            \"sequenceNumber\": 0\n"
                "                        },\n"
                "                        {\n"
                "                            \"id\": 11040,\n"
                "                            \"sectionTrackId\": 1165,\n"
                "                            \"nodeId\": 24,\n"
                "                            \"nodeTrackId\": 25,\n"
                "                            \"formationId\": 1187,\n"
                "                            \"arrivalTime\": \"2003-05-01T00:10:00\",\n"
                "                            \"departureTime\": \"2003-05-01T00:10:00\",\n"
                "                            \"minimumRunTime\": \"P0D\",\n"
                "                            \"minimumStopTime\": \"P0D\",\n"
                "                            \"stopStatus\": \"passing\",\n"
                "                            \"sequenceNumber\": 1\n"
                "                        },\n"
                "                        {\n"
                "                            \"id\": 3152,\n"
                "                            \"sectionTrackId\": 1166,\n"
                "                            \"nodeId\": 10,\n"
                "                            \"nodeTrackId\": 12,\n"
                "                            \"formationId\": null,\n"
                "                            \"arrivalTime\": \"2003-05-01T00:19:00\",\n"
                "                            \"departureTime\": \"2003-05-01T00:19:00\",\n"
                "                            \"minimumRunTime\": \"PT9M\",\n"
                "                            \"minimumStopTime\": \"P0D\",\n"
                "                            \"stopStatus\": \"commercialStop\",\n"
                "                            \"sequenceNumber\": 2\n"
                "                        }\n"
                "                    ],\n"
                "                    \"debugString\": \"RVZH_3_1_J03 tt_(S)\"\n"
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

        test_route = UpdateTrainRoute(
            end_train_path_node_id=end_train_path_node_id,
            start_train_path_node_id=start_train_path_node_id,
            routing_edges=routing_edges)

        self.interface_to_viriato.reroute_train(train_id, test_route)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        expected_routing_edge_body = [dict(nodeId=7, startNodeTrackId=8, endSectionTrackId=1165),
                                      dict(nodeId=24, startSectionTrackId=1165, endNodeTrackId=25),
                                      dict(nodeId=24, startNodeTrackId=25, endSectionTrackId=1166),
                                      dict(nodeId=10, startSectionTrackId=1166, endNodeTrackId=12)]

        self.assertEqual(get_api_url() + "/trains/{0}/train-path-nodes:reroute".format(train_id),
                         session_obj._RerouteTrainTestMockSession__last_request)
        self.assertListEqual(session_obj._RerouteTrainTestMockSession__last_body['routingEdges'],
                             expected_routing_edge_body)
        self.assertDictEqual(session_obj._RerouteTrainTestMockSession__last_body["routingEdges"][0],
                             expected_routing_edge_body[0])
        self.assertEqual(session_obj._RerouteTrainTestMockSession__last_body["startTrainPathNodeId"], 2424)
        self.assertEqual(session_obj._RerouteTrainTestMockSession__last_body["endTrainPathNodeId"], 3152)

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def test_reroute_train_response(self, mocked_session):
        train_id = 2060
        start_train_path_node_id = 2424
        end_train_path_node_id = 3152
        routing_edges = [OutgoingRoutingEdge(node_id=7, start_node_track_id=8, end_section_track_id=1165),
                         IncomingRoutingEdge(node_id=24, start_section_track_id=1165, end_node_track_id=25),
                         OutgoingRoutingEdge(node_id=24, start_node_track_id=25, end_section_track_id=1166),
                         IncomingRoutingEdge(node_id=10, start_section_track_id=1166, end_node_track_id=12)]

        test_route = UpdateTrainRoute(
            end_train_path_node_id=end_train_path_node_id,
            start_train_path_node_id=start_train_path_node_id,
            routing_edges=routing_edges)

        rerouted_algorithm_train = self.interface_to_viriato.reroute_train(train_id, test_route)

        self.assertEqual(rerouted_algorithm_train.id, 3516)
        self.assertEqual(rerouted_algorithm_train.debug_string, "RVZH_3_1_J03 tt_(S)")
        self.assertEqual(rerouted_algorithm_train.code, "TestRerouteTrain")
        self.assertIsInstance(rerouted_algorithm_train.train_path_nodes, list)
        self.assertIsInstance(rerouted_algorithm_train.train_path_nodes[0], AlgorithmTrainPathNode)
        self.assertEqual(rerouted_algorithm_train.train_path_nodes[0].id, 2424)

    @mock.patch('requests.Session', side_effect=RerouteTrainTestMockSession)
    def tearDown(self, mocked_session) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
