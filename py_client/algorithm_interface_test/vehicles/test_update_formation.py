import unittest
from unittest import mock

from py_client.aidm import AlgorithmTrain, AlgorithmTrainPathNode
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import SessionMockTestBase, get_api_url


class TestUpdateFormation(unittest.TestCase):
    class UpdateFormationTestMockSession(SessionMockTestBase):
        def put(self, request, json):
            self._last_body = json
            self._last_request = request
            if json == {"formationID": 1551, "fromTrainPathNodeID": 11037, "toTrainPathNodeID": 11038}:
                json_string = ("{\n"
                               "  \"id\": 11040,\n"
                               "  \"trainPathNodes\": [\n"
                               "    {\n"
                               "      \"id\": 11037,\n"
                               "      \"sectionTrackId\": null,\n"
                               "      \"nodeId\": 7,\n"
                               "      \"nodeTrackId\": 8,\n"
                               "      \"formationId\": 1551,\n"
                               "      \"arrivalTime\": \"2003-09-01T04:10:00\",\n"
                               "      \"departureTime\": \"2003-09-01T04:10:00\",\n"
                               "      \"minimumRunTime\": null,\n"
                               "      \"minimumStopTime\": \"P0D\",\n"
                               "      \"stopStatus\": \"commercialStop\",\n"
                               "      \"sequenceNumber\": 0\n"
                               "    },\n"
                               "    {\n"
                               "      \"id\": 11038,\n"
                               "      \"sectionTrackId\": 1175,\n"
                               "      \"nodeId\": 15,\n"
                               "      \"nodeTrackId\": 16,\n"
                               "      \"formationId\": 5557,\n"
                               "      \"arrivalTime\": \"2003-09-01T04:14:00\",\n"
                               "      \"departureTime\": \"2003-09-01T04:14:00\",\n"
                               "      \"minimumRunTime\": \"PT4M\",\n"
                               "      \"minimumStopTime\": \"P0D\",\n"
                               "      \"stopStatus\": \"passing\",\n"
                               "      \"sequenceNumber\": 1\n"
                               "    },\n"
                               "    {\n"
                               "      \"id\": 11039,\n"
                               "      \"sectionTrackId\": 1174,\n"
                               "      \"nodeId\": 10,\n"
                               "      \"nodeTrackId\": 12,\n"
                               "      \"formationId\": null,\n"
                               "      \"arrivalTime\": \"2003-09-01T04:19:00\",\n"
                               "      \"departureTime\": \"2003-09-01T04:19:00\",\n"
                               "      \"minimumRunTime\": \"PT5M\",\n"
                               "      \"minimumStopTime\": \"P0D\",\n"
                               "      \"stopStatus\": \"commercialStop\",\n"
                               "      \"sequenceNumber\": 2\n"
                               "    }\n"
                               "  ],\n"
                               "  \"code\": \"RVZH_15_1_J03\",\n"
                               "  \"debugString\": \"RVZH_15_1_J03xxxx tt_(S)\"\n"
                               "}")
            elif json == {"formationID": 1551, "fromTrainPathNodeID": 11037}:
                json_string = ("{\n"
                               "  \"id\": 11040,\n"
                               "  \"trainPathNodes\": [\n"
                               "    {\n"
                               "      \"id\": 11037,\n"
                               "      \"sectionTrackId\": null,\n"
                               "      \"nodeId\": 7,\n"
                               "      \"nodeTrackId\": 8,\n"
                               "      \"formationId\": 1551,\n"
                               "      \"arrivalTime\": \"2003-09-01T04:10:00\",\n"
                               "      \"departureTime\": \"2003-09-01T04:10:00\",\n"
                               "      \"minimumRunTime\": null,\n"
                               "      \"minimumStopTime\": \"P0D\",\n"
                               "      \"stopStatus\": \"commercialStop\",\n"
                               "      \"sequenceNumber\": 0\n"
                               "    },\n"
                               "    {\n"
                               "      \"id\": 11038,\n"
                               "      \"sectionTrackId\": 1175,\n"
                               "      \"nodeId\": 15,\n"
                               "      \"nodeTrackId\": 16,\n"
                               "      \"formationId\": 1551,\n"
                               "      \"arrivalTime\": \"2003-09-01T04:14:00\",\n"
                               "      \"departureTime\": \"2003-09-01T04:14:00\",\n"
                               "      \"minimumRunTime\": \"PT4M\",\n"
                               "      \"minimumStopTime\": \"P0D\",\n"
                               "      \"stopStatus\": \"passing\",\n"
                               "      \"sequenceNumber\": 1\n"
                               "    },\n"
                               "    {\n"
                               "      \"id\": 11039,\n"
                               "      \"sectionTrackId\": 1174,\n"
                               "      \"nodeId\": 10,\n"
                               "      \"nodeTrackId\": 12,\n"
                               "      \"formationId\": null,\n"
                               "      \"arrivalTime\": \"2003-09-01T04:19:00\",\n"
                               "      \"departureTime\": \"2003-09-01T04:19:00\",\n"
                               "      \"minimumRunTime\": \"PT5M\",\n"
                               "      \"minimumStopTime\": \"P0D\",\n"
                               "      \"stopStatus\": \"commercialStop\",\n"
                               "      \"sequenceNumber\": 2\n"
                               "    }\n"
                               "  ],\n"
                               "  \"code\": \"RVZH_15_1_J03\",\n"
                               "  \"debugString\": \"RVZH_15_1_J03 tt_(S)\"\n"
                               "}")
            else:
                raise NotImplementedError("This Test Case is not defined")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=UpdateFormationTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=UpdateFormationTestMockSession)
    def test_update_formation_request_with_with_four_parameters(self, mocked_get_obj):
        train_id = 1234
        from_train_path_node_id = 11037
        to_train_path_node_id = 11038
        formation_id = 1551

        self.interface_to_viriato.update_train_formation(
            train_id,
            from_train_path_node_id,
            to_train_path_node_id,
            formation_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + '/trains/1234/train-path-nodes:update-formation')
        self.assertDictEqual(
            session_obj.last_body,
            dict(formationID=1551, fromTrainPathNodeID=11037, toTrainPathNodeID=11038))

    @mock.patch('requests.Session', side_effect=UpdateFormationTestMockSession)
    def test_update_formation_request_with_with_three_parameters(self, mocked_get_obj):
        train_id = 999
        from_train_path_node_id = 11037
        formation_id = 1551

        self.interface_to_viriato.update_train_formation(train_id, from_train_path_node_id, formation_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + '/trains/999/train-path-nodes:update-formation')
        self.assertDictEqual(session_obj.last_body, dict(formationID=1551, fromTrainPathNodeID=11037))

    @mock.patch('requests.Session', side_effect=UpdateFormationTestMockSession)
    def test_update_formation_response_with_with_four_parameters(self, mocked_get_obj):
        train_id = 1234
        from_train_path_node_id = 11037
        to_train_path_node_id = 11038
        formation_id = 1551

        updated_train = self.interface_to_viriato.update_train_formation(
            train_id,
            from_train_path_node_id,
            to_train_path_node_id,
            formation_id)

        self.assertIsInstance(updated_train, AlgorithmTrain)
        self.assertEqual(updated_train.id, 11040)
        self.assertEqual(updated_train.debug_string, "RVZH_15_1_J03xxxx tt_(S)")
        self.assertEqual(updated_train.code, "RVZH_15_1_J03")
        self.assertIsInstance(updated_train.train_path_nodes, list)
        self.assertEqual(len(updated_train.train_path_nodes), 3)

        first_train_path_node = updated_train.train_path_nodes[0]
        self.assertIsInstance(first_train_path_node, AlgorithmTrainPathNode)
        self.assertEqual(first_train_path_node.id, 11037)
        self.assertEqual(first_train_path_node.node_id, 7)

    @mock.patch('requests.Session', side_effect=UpdateFormationTestMockSession)
    def test_update_formation_response_with_with_three_parameters(self, mocked_get_obj):
        train_id = 1234
        from_train_path_node_id = 11037
        formation_id = 1551

        updated_train = self.interface_to_viriato.update_train_formation(train_id, from_train_path_node_id, formation_id)

        self.assertIsInstance(updated_train, AlgorithmTrain)
        self.assertEqual(updated_train.debug_string, "RVZH_15_1_J03 tt_(S)")
        self.assertEqual(updated_train.id, 11040)
        self.assertIsInstance(updated_train.train_path_nodes, list)
        self.assertEqual(len(updated_train.train_path_nodes), 3)

        first_train_path_node = updated_train.train_path_nodes[0]
        self.assertIsInstance(first_train_path_node, AlgorithmTrainPathNode)
        self.assertEqual(first_train_path_node.id, 11037)
        self.assertEqual(first_train_path_node.node_id, 7)

    @mock.patch('requests.Session', side_effect=UpdateFormationTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
