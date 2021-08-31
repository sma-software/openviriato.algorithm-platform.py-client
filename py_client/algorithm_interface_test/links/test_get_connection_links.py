import datetime
import unittest
from unittest import mock

from py_client.aidm import TimeWindow, AlgorithmConnectionLink
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import SessionMockTestBase, get_api_url


class TestGetConnectionLinks(unittest.TestCase):
    class GetConnectionLinksTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self._last_body = params
            self._last_request = request
            if params["fromTime"] == params["toTime"]:
                json_string = "[]"
            else:
                json_string = ("[\n"
                               "{\n"
                               "  \"MinimumDuration\": \"PT6M\",\n"
                               "  \"MaximumDeviation\": \"PT13M\",\n"
                               "  \"weight\": 1,\n"
                               "  \"fromNodeId\": 281,\n"
                               "  \"fromTrainId\": 2417,\n"
                               "  \"fromTrainPathNodeId\": 1689,\n"
                               "  \"toNodeId\": 281,\n"
                               "  \"toTrainId\": 3873,\n"
                               "  \"toTrainPathNodeId\": 3145,\n"
                               "  \"type\": \"connection\",\n"
                               "  \"debugString\": \"link: FV_8_J03, 85JE, planned arrival: 01.05.2003 "
                               "07:01.2 - FV_10_J03, 85JE, planned departure: 01.05.2003 07:31.2\"\n"
                               "},\n"
                               "{\n"
                               "  \"MinimumDuration\": \"PT6M\",\n"
                               "  \"MaximumDeviation\": null,\n"
                               "  \"weight\": null,\n"
                               "  \"fromNodeId\": 281,\n"
                               "  \"fromTrainId\": 2417,\n"
                               "  \"fromTrainPathNodeId\": 1689,\n"
                               "  \"toNodeId\": 281,\n"
                               "  \"toTrainId\": 3873,\n"
                               "  \"toTrainPathNodeId\": 3145,\n"
                               "  \"type\": \"connection\",\n"
                               "  \"debugString\": \"link: FV_8_J03, 85JE, planned arrival: 01.05.2003 "
                               "07:01.2 - FV_10_J03, 85JE, planned departure: 01.05.2003 07:31.2\"\n"
                               "}\n"
                               "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetConnectionLinksTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetConnectionLinksTestMockSession)
    def test_get_links_request(self, mocked_get_obj):
        time_window = TimeWindow(
            from_time=datetime.datetime(2000, 1, 1, 1, 1), to_time=datetime.datetime(2004, 1, 1, 0, 0)
        )

        self.interface_to_viriato.get_connection_links(time_window)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + '/links')
        self.assertDictEqual(
            session_obj.last_body,
            dict(fromTime="2000-01-01T01:01:00", toTime="2004-01-01T00:00:00", linkType='connection', nodeFilter=None)
        )

    @mock.patch('requests.Session', side_effect=GetConnectionLinksTestMockSession)
    def test_get_links_one_link_as_response(self, mocked_get_obj):
        time_window = TimeWindow(
            from_time=datetime.datetime(2000, 1, 1, 1, 1), to_time=datetime.datetime(2004, 1, 1, 0, 0)
        )

        listed_algorithm_links = self.interface_to_viriato.get_connection_links(time_window)

        self.assertIsInstance(listed_algorithm_links, list)
        self.assertEqual(listed_algorithm_links.__len__(), 2)

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

    @mock.patch('requests.Session', side_effect=GetConnectionLinksTestMockSession)
    def test_get_links_empty_list_as_response(self, mocked_get_obj):
        time_window = TimeWindow(
            from_time=datetime.datetime(2000, 1, 1, 1, 1), to_time=datetime.datetime(2000, 1, 1, 1, 1)
        )

        listed_algorithm_links = self.interface_to_viriato.get_connection_links(time_window)

        self.assertIsInstance(listed_algorithm_links, list)
        self.assertEqual(listed_algorithm_links.__len__(), 0)

    @mock.patch('requests.Session', side_effect=GetConnectionLinksTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
