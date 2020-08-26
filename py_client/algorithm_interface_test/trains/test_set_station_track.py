from unittest import mock, TestCase

import py_client.aidm.aidm_algorithm_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client import algorithm_interface
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestSetSectionTrack(TestCase):
    class SetSectionTrackTestMockSession(SessionMockTestBase):
        # to replace session.get:
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = ('{\n'
                           '  "id": 2060,\n'
                           '  "trainPathNodes": [\n'
                           '    {\n'
                           '      "id": 1332,\n'
                           '      "SectionTrackId": null,\n'
                           '      "nodeId": 18,\n'
                           '      "nodeTrackId": null,\n'
                           '      "formationId": 1187,\n'
                           '      "arrivalTime": "2003-05-01T00:05:00",\n'
                           '      "departureTime": "2003-05-01T00:05:00",\n'
                           '      "minimumRunTime": null,\n'
                           '      "minimumStopTime": "P0D",\n'
                           '      "stopStatus": "commercialStop",\n'
                           '      "sequenceNumber": 0\n'
                           '    },\n'
                           '    {\n'
                           '      "id": 1696,\n'
                           '      "SectionTrackId": 1172,\n'
                           '      "nodeId": 10,\n'
                           '      "nodeTrackId": null,\n'
                           '      "formationId": null,\n'
                           '      "arrivalTime": "2003-05-01T00:10:00",\n'
                           '      "departureTime": "2003-05-01T00:10:00",\n'
                           '      "minimumRunTime": "PT5M",\n'
                           '      "minimumStopTime": "P0D",\n'
                           '      "stopStatus": "commercialStop",\n'
                           '      "sequenceNumber": 1\n'
                           '    }\n'
                           '  ],\n'
                           '  "debugString": "SetSectionTrackTestMockSessionString"\n'
                           '}')
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=SetSectionTrackTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=SetSectionTrackTestMockSession)
    def test_set_section_track_request(self, mocked_get_obj) -> None:
        test_dict = dict(trainPathNodeId=1696, sectionTrackId=1172)

        self.interface_to_viriato.set_section_track(test_dict['trainPathNodeId'], test_dict['sectionTrackId'])

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._SetSectionTrackTestMockSession__last_request,
                         get_api_url() + '/set-section-track')
        self.assertDictEqual(session_obj._SetSectionTrackTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=SetSectionTrackTestMockSession)
    def test_set_section_track_response(self, mocked_get_obj):
        train_path_node_id = 1
        section_track_id = 1

        test_algorithm_train = self.interface_to_viriato.set_section_track(train_path_node_id, section_track_id)

        self.assertIsInstance(test_algorithm_train, py_client.aidm.aidm_algorithm_classes.AlgorithmTrain)
        self.assertEqual(2060, test_algorithm_train.id)
        self.assertEqual(test_algorithm_train.debug_string, 'SetSectionTrackTestMockSessionString')

    @mock.patch('requests.Session', side_effect=SetSectionTrackTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
