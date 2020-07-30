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
                           '  "ID": 2060,\n'
                           '  "TrainPathNodes": [\n'
                           '    {\n'
                           '      "ID": 1332,\n'
                           '      "SectionTrackID": null,\n'
                           '      "node_id": 18,\n'
                           '      "node_track_id": null,\n'
                           '      "FormationID": 1187,\n'
                           '      "ArrivalTime": "2003-05-01T00:05:00",\n'
                           '      "DepartureTime": "2003-05-01T00:05:00",\n'
                           '      "MinimumRunTime": null,\n'
                           '      "MinimumStopTime": "P0D",\n'
                           '      "StopStatus": "commercialStop",\n'
                           '      "SequenceNumber": 0\n'
                           '    },\n'
                           '    {\n'
                           '      "ID": 1696,\n'
                           '      "SectionTrackID": 1172,\n'
                           '      "node_id": 10,\n'
                           '      "node_track_id": null,\n'
                           '      "FormationID": null,\n'
                           '      "ArrivalTime": "2003-05-01T00:10:00",\n'
                           '      "DepartureTime": "2003-05-01T00:10:00",\n'
                           '      "MinimumRunTime": "PT5M",\n'
                           '      "MinimumStopTime": "P0D",\n'
                           '      "StopStatus": "commercialStop",\n'
                           '      "SequenceNumber": 1\n'
                           '    }\n'
                           '  ],\n'
                           '  "DebugString": "SetSectionTrackTestMockSessionString"\n'
                           '}')
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=SetSectionTrackTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=SetSectionTrackTestMockSession)
    def test_set_section_track_request(self, mocked_get_obj) -> None:
        test_dict = dict(TrainPathNodeID=1696, SectionTrackID=1172)

        self.interface_to_viriato.set_section_track(test_dict['TrainPathNodeID'], test_dict['SectionTrackID'])

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
