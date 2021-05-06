import datetime
import unittest
from unittest import mock

from py_client.aidm import TimeWindow, AlgorithmAwaitArrivalLink
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper import SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import SessionMockTestBase, get_api_url


class TestGetAwaitArrivalLinks(unittest.TestCase):
    class GetAwaitArrivalLinksTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self._last_body = params
            self._last_request = request
            if params["fromTime"] == params["toTime"]:
                json_string = "[]"
            else:
                json_string = ("[\n"
                               "{\n"
                               "  \"MinimumDuration\": \"PT10M\",\n"
                               "  \"fromNodeId\": 161,\n"
                               "  \"fromTrainId\": 5329,\n"
                               "  \"fromTrainPathNodeId\": 4965,\n"
                               "  \"toNodeId\": 161,\n"
                               "  \"toTrainId\": 2417,\n"
                               "  \"toTrainPathNodeId\": 1323,\n"
                               "  \"type\": \"awaitArrival\",\n"
                               "  \"debugString\": \"link: FV_9_J03, 85AR, planned arrival: 01.05.2003 "
                               "06:03.9 - FV_8_J03, 85AR, planned departure: 01.05.2003 07:00.0\"\n"
                               "}\n"
                               "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetAwaitArrivalLinksTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetAwaitArrivalLinksTestMockSession)
    def test_get_await_arrival_links(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1),
                                 to_time=datetime.datetime(2004, 1, 1, 0, 0))

        self.interface_to_viriato.get_await_arrival_links(time_window)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + '/links')
        self.assertDictEqual(session_obj.last_body,
                             dict(fromTime="2000-01-01T01:01:00",
                                  toTime="2004-01-01T00:00:00",
                                  linkType='awaitArrival'))

    @mock.patch('requests.Session', side_effect=GetAwaitArrivalLinksTestMockSession)
    def test_get_await_arrival_links_one_link_as_response(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1),
                                 to_time=datetime.datetime(2004, 1, 1, 0, 0))

        listed_algorithm_links = self.interface_to_viriato.get_await_arrival_links(time_window)

        self.assertIsInstance(listed_algorithm_links, list)
        self.assertEqual(listed_algorithm_links.__len__(), 1)

        self.assertIsInstance(listed_algorithm_links[0], AlgorithmAwaitArrivalLink)
        algorithm_connection_link: AlgorithmAwaitArrivalLink = listed_algorithm_links[0]
        self.assertEqual(algorithm_connection_link.from_node_id, 161)
        self.assertEqual(algorithm_connection_link.from_train_id, 5329)
        self.assertEqual(algorithm_connection_link.from_train_path_node_id, 4965)
        self.assertEqual(algorithm_connection_link.to_node_id, 161)
        self.assertEqual(algorithm_connection_link.to_train_id, 2417)
        self.assertEqual(algorithm_connection_link.to_train_path_node_id, 1323)
        self.assertEqual(algorithm_connection_link.minimum_duration, datetime.timedelta(seconds=600))

    @mock.patch('requests.Session', side_effect=GetAwaitArrivalLinksTestMockSession)
    def test_get_await_arrival_links_empty_list_as_response(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1),
                                 to_time=datetime.datetime(2000, 1, 1, 1, 1))

        listed_algorithm_links = self.interface_to_viriato.get_await_arrival_links(time_window)

        self.assertIsInstance(listed_algorithm_links, list)
        self.assertEqual(listed_algorithm_links.__len__(), 0)

    @mock.patch('requests.Session', side_effect=GetAwaitArrivalLinksTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
