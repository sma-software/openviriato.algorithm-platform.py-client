"""
A test script that requires an REST-API of the VIRIATO-Algorithm Platform
"""

import unittest
from datetime import datetime

import AlgorithmInterface.AlgorithmInterface
from AIDMClasses import AIDM_classes
from CommunicationLayer import AlgorithmInterfaceCommunicationLayer


def get_url_str():
    url_str = 'http://localhost:8080'
    return url_str


class TestObjectInitialisation(unittest.TestCase):
    # test for the object creation:
    def test_initialisation_in_with(self):
        with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
            self.assertEqual(interface_to_viriato.base_url, get_url_str())

    # fails on purpose:
    def test_if_initialisation_with_int_fails(self):
        url_nr = 952022
        with self.assertRaises(AssertionError):
            with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(url_nr) as interface_to_viriato:
                self.assertEqual(interface_to_viriato.base_url, get_url_str())


class TestUserNotifications(unittest.TestCase):

    def test_user_notification_with_str(self):
        with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
            interface_to_viriato.notify_user('hi', 'it works')

    def test_user_notifications_wrong_type(self):
        with self.assertRaises(AssertionError):
            with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
                interface_to_viriato.notify_user(1, 2)


class TestShowStatusMessage(unittest.TestCase):

    def test_show_status_message_one_str(self):
        with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
            interface_to_viriato.show_status_message('Foo bar')

    def test_show_status_message_two_str(self):
        with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
            interface_to_viriato.show_status_message('Foo', 'bar')

    def test_user_notifications_wrong_type_one_param(self):
        with self.assertRaises(AssertionError):
            with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
                interface_to_viriato.show_status_message(1)

    def test_user_notifications_wrong_type_two_param(self):
        with self.assertRaises(AssertionError):
            with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
                interface_to_viriato.show_status_message('one', 1)


class TestGetDirectedSectionTracks(unittest.TestCase):
    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    def setUp(self):
        self.interface_to_viriato = AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(get_url_str())

    def tearDown(self) -> None:
        self.interface_to_viriato.__exit__(None, None, None)

    def test_get_directed_section_tracks_with_range(self):
        # lets test the robustness:
        track_list = []
        with self.assertRaises(AlgorithmInterfaceCommunicationLayer.AlgorithmPlatformError):
            for i in range(1, 50):
                for j in range(1, 50):
                    if i == j:
                        continue
                directed_section_tracks = self.interface_to_viriato.get_directed_section_tracks(i, j)
                track_list.append(directed_section_tracks)

                self.assertGreater(len(track_list), 0, '0 dir-Tracks found range of i = {0} and j {1}'.format(100, 100))

    def test_get_directed_section_tracks_str_parameters(self):
        with self.assertRaises(AssertionError):
            directed_section_tracks = self.interface_to_viriato.get_directed_section_tracks('A', 'b')


def test_get_parallel_section_tracks(interface_to_viriato) -> None:
    for i in range(1, 1000):
        try:
            track_list = interface_to_viriato.get_parallel_section_tracks(i)
            # if len(track_list) > 0:
            #    for idx in range(len(track_list)):
            #       print(track_list[idx].ID)
        except AlgorithmInterfaceCommunicationLayer.AlgorithmPlatformError:
            i
    print('test_get_parallel_section_tracks complete')


def test_algorithm_node_object(node_id=1, code_string='someTestNodeID', debug_string='', node_tracks=[]):
    test_node = AIDM_classes.AlgorithmNode(node_id, code_string, debug_string, node_tracks)
    print(test_node.ID)
    print(test_node.DebugString)
    print(test_node.Code)


def test_train_cancellations(interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface) -> None:
    for i in range(500, 5000):
        try:
            interface_to_viriato.cancel_train_to(train_path_node_id=i)
        except AlgorithmInterfaceCommunicationLayer.AlgorithmPlatformError:
            i
    for i in range(500, 5000):
        try:
            obj = interface_to_viriato.cancel_train_from(train_path_node_id=i)
        except AlgorithmInterfaceCommunicationLayer.AlgorithmPlatformError:
            i


def main():
    unittest.main()


def main_void():
    url_str = 'http://localhost:8080'
    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    test_object_initialisation(url_str)

    with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
        test_train_cancellations(interface_to_viriato)
        print('test_train_cancellations complete')

    with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
        # try to retrieve the url:
        print(interface_to_viriato.base_url)
        print('url retrieve test complete')
        test_user_notifications(interface_to_viriato)
        try:
            print(interface_to_viriato.get_train_classifications())
        except AlgorithmInterfaceCommunicationLayer.AlgorithmPlatformError:
            print('Train classifications not configured')

    with test_object_initialisation(url_str) as interface_to_viriato:
        test_get_parallel_section_tracks(interface_to_viriato)
        test_get_directed_section_tracks(interface_to_viriato)

    with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
        test_get_node_and_get_neighbor_nodes(interface_to_viriato)

    # other tests for the data types
    test_algorithm_node_object(node_id=1, code_string='TestNodeID', debug_string='test_node', node_tracks=['A', 'B'])
    AIDM_classes.UpdateTrainTimesNode(datetime(year=2001, month=1, day=1, hour=1, minute=1, second=1),
                                      datetime(year=2001, month=1, day=1, hour=1, minute=1, second=1), 1)


if __name__ == '__main__':
    main()
