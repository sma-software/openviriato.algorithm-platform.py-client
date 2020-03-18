from unittest import mock, TestCase

import AlgorithmInterface.AlgorithmInterface
import unit_testing.test_AlgorithmInterface_with_mock.unit_testing_requisites.SessionMockFactory as SessionMockFactory
from AIDMClasses import AIDM_classes
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_requisites.unit_testing_with_mock_helpers import \
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
                           '      "NodeID": 18,\n'
                           '      "NodeTrackID": null,\n'
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
                           '      "NodeID": 10,\n'
                           '      "NodeTrackID": null,\n'
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

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=SetSectionTrackTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=SetSectionTrackTestMockSession)
    def test_set_section_track_request(self, mocked_get_obj) -> None:
        test_dict = dict(TrainPathNodeID=1696, SectionTrackID=1172)

        self.interface_to_viriato.set_section_track(test_dict['TrainPathNodeID'], test_dict['SectionTrackID'])

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession

        self.assertEqual(session_obj._SetSectionTrackTestMockSession__last_request,
                         get_api_url() + '/set-section-track')
        self.assertDictEqual(session_obj._SetSectionTrackTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=SetSectionTrackTestMockSession)
    def test_set_section_track_response(self, mocked_get_obj):
        TrainPathNodeID = 1
        SectionTrackID = 1

        test_algorithm_train = self.interface_to_viriato.set_section_track(TrainPathNodeID, SectionTrackID)

        self.assertIsInstance(test_algorithm_train, AIDM_classes.AlgorithmTrain)
        self.assertEqual(2060, test_algorithm_train.ID)
        self.assertEqual(test_algorithm_train.DebugString, 'SetSectionTrackTestMockSessionString')

    @mock.patch('requests.Session', side_effect=SetSectionTrackTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
