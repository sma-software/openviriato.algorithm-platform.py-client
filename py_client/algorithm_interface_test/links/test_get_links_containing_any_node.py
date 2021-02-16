import datetime
import unittest
from unittest import mock

from py_client.aidm import TimeWindow, AlgorithmAwaitArrivalLink, AlgorithmConnectionLink
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import SessionMockTestBase, get_api_url


class TestGetLinksContainingAnyNode(unittest.TestCase):
    class GetLinksContainingAnyNodeTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self._last_body = params
            self._last_request = request
            if params["fromTime"] == params["toTime"]:
                json_string = "[]"
            else:
                json_string = ("[\n"
                               "{\n"
                               "  \"minimumDuration\": \"PT6M\",\n"
                               "  \"maximumDeviation\": \"PT13M\",\n"
                               "  \"weight\": 1,\n"
                               "  \"fromNodeId\": 281,\n"
                               "  \"fromTrainId\": 2417,\n"
                               "  \"fromTrainPathNodeId\": 1689,\n"
                               "  \"toNodeId\": 281,\n"
                               "  \"toTrainId\": 3873,\n"
                               "  \"toTrainPathNodeId\": 3145,\n"
                               "  \"linkType\": \"connection\",\n"
                               "  \"debugString\": \"link: FV_8_J03, 85JE, planned arrival: 01.05.2003 "
                               "07:01.2 - FV_10_J03, 85JE, planned departure: 01.05.2003 07:31.2\"\n"
                               "},\n"
                               "{\n"
                               "  \"minimumDuration\": \"PT6M\",\n"
                               "  \"maximumDeviation\": null,\n"
                               "  \"weight\": null,\n"
                               "  \"fromNodeId\": 281,\n"
                               "  \"fromTrainId\": 2417,\n"
                               "  \"fromTrainPathNodeId\": 1689,\n"
                               "  \"toNodeId\": 281,\n"
                               "  \"toTrainId\": 3873,\n"
                               "  \"toTrainPathNodeId\": 3145,\n"
                               "  \"linkType\": \"connection\",\n"
                               "  \"debugString\": \"link: FV_8_J03, 85JE, planned arrival: 01.05.2003 "
                               "07:01.2 - FV_10_J03, 85JE, planned departure: 01.05.2003 07:31.2\"\n"
                               "},\n"
                               "{\n"
                               "  \"minimumDuration\": \"PT10M\",\n"
                               "  \"fromNodeId\": 161,\n"
                               "  \"fromTrainId\": 5329,\n"
                               "  \"fromTrainPathNodeId\": 4965,\n"
                               "  \"toNodeId\": 161,\n"
                               "  \"toTrainId\": 2417,\n"
                               "  \"toTrainPathNodeId\": 1323,\n"
                               "  \"linkType\": \"awaitArrival\",\n"
                               "  \"debugString\": \"link: FV_9_J03, 85AR, planned arrival: 01.05.2003 "
                               "06:03.9 - FV_8_J03, 85AR, planned departure: 01.05.2003 07:00.0\"\n"
                               "}\n"
                               "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetLinksContainingAnyNodeTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetLinksContainingAnyNodeTestMockSession)
    def test_get_links_containing_any_node_request(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1),
                                 to_time=datetime.datetime(2004, 1, 1, 0, 0))
        node_ids = [12]

        self.interface_to_viriato.get_links_containing_any_node(time_window, node_ids)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + '/links')
        self.assertDictEqual(session_obj.last_body,
                             dict(fromTime="2000-01-01T01:01:00",
                                  toTime="2004-01-01T00:00:00",
                                  nodeFilter=[12]))

    @mock.patch('requests.Session', side_effect=GetLinksContainingAnyNodeTestMockSession)
    def test_get_links_containing_any_node_two_links_as_response(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1),
                                 to_time=datetime.datetime(2004, 1, 1, 0, 0))
        node_ids = [12]

        listed_algorithm_links = self.interface_to_viriato.get_links_containing_any_node(time_window, node_ids)

        self.assertIsInstance(listed_algorithm_links, list)
        self.assertEqual(listed_algorithm_links.__len__(), 3)

        algorithm_connection_link: AlgorithmConnectionLink = listed_algorithm_links[0]
        self.assertIsInstance(algorithm_connection_link, AlgorithmConnectionLink)
        self.assertEqual(
            algorithm_connection_link.debug_string,
            "link: FV_8_J03, 85JE, planned arrival: 01.05.2003 07:01.2 - FV_10_J03, 85JE,"
            " planned departure: 01.05.2003 07:31.2")
        self.assertEqual(algorithm_connection_link.from_node_id, 281)
        self.assertEqual(algorithm_connection_link.from_train_id, 2417)
        self.assertEqual(algorithm_connection_link.from_train_path_node_id, 1689)
        self.assertEqual(algorithm_connection_link.to_node_id, 281)
        self.assertEqual(algorithm_connection_link.to_train_id, 3873)
        self.assertEqual(algorithm_connection_link.to_train_path_node_id, 3145)
        self.assertEqual(algorithm_connection_link.weight, 1)
        self.assertEqual(algorithm_connection_link.minimum_duration, datetime.timedelta(minutes=6))
        self.assertEqual(algorithm_connection_link.maximum_deviation, datetime.timedelta(minutes=13))

        algorithm_connection_link: AlgorithmConnectionLink = listed_algorithm_links[1]
        self.assertIsInstance(algorithm_connection_link, AlgorithmConnectionLink)
        self.assertEqual(
            algorithm_connection_link.debug_string,
            "link: FV_8_J03, 85JE, planned arrival: 01.05.2003 07:01.2 - FV_10_J03, 85JE,"
            " planned departure: 01.05.2003 07:31.2")
        self.assertEqual(algorithm_connection_link.from_node_id, 281)
        self.assertEqual(algorithm_connection_link.from_train_id, 2417)
        self.assertEqual(algorithm_connection_link.from_train_path_node_id, 1689)
        self.assertEqual(algorithm_connection_link.to_node_id, 281)
        self.assertEqual(algorithm_connection_link.to_train_id, 3873)
        self.assertEqual(algorithm_connection_link.to_train_path_node_id, 3145)
        self.assertEqual(algorithm_connection_link.minimum_duration, datetime.timedelta(minutes=6))
        self.assertEqual(algorithm_connection_link.weight, None)
        self.assertIsNone(algorithm_connection_link.maximum_deviation, None)

        self.assertIsInstance(listed_algorithm_links[2], AlgorithmAwaitArrivalLink)
        algorithm_connection_link: AlgorithmAwaitArrivalLink = listed_algorithm_links[2]
        self.assertEqual(algorithm_connection_link.from_node_id, 161)
        self.assertEqual(algorithm_connection_link.from_train_id, 5329)
        self.assertEqual(algorithm_connection_link.from_train_path_node_id, 4965)
        self.assertEqual(algorithm_connection_link.to_node_id, 161)
        self.assertEqual(algorithm_connection_link.to_train_id, 2417)
        self.assertEqual(algorithm_connection_link.to_train_path_node_id, 1323)
        self.assertEqual(algorithm_connection_link.minimum_duration, datetime.timedelta(seconds=600))

    @mock.patch('requests.Session', side_effect=GetLinksContainingAnyNodeTestMockSession)
    def get_links_containing_any_node_empty_list_as_response(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1),
                                 to_time=datetime.datetime(2000, 1, 1, 1, 1))
        node_ids = [12]

        listed_algorithm_links = self.interface_to_viriato.get_links_containing_any_node(time_window, node_ids)

        self.assertIsInstance(listed_algorithm_links, list)
        self.assertEqual(listed_algorithm_links.__len__(), 0)

    @mock.patch('requests.Session', side_effect=GetLinksContainingAnyNodeTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
