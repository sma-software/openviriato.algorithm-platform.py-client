import unittest
import os

import unit_testing_with_mock.test_infrastructure_request.test_get_directed_section_tracks
import unit_testing_with_mock.test_interface_init as test_interface_init
import unit_testing_with_mock.test_notifications as test_notifications


class InitTest(test_interface_init.TestObjectInitialisation):
    pass


class NotificationTest(test_notifications.TestUserNotifications):
    pass


class ShowMessageTest(test_notifications.TestShowStatusMessage):
    pass


class DirectedTrack(
    unit_testing_with_mock.test_infrastructure_request.test_get_directed_section_tracks.TestGetDirectedSectionTracks):
    pass


if __name__ == '__main__':

    unittest.main()
    print(os.getcwd())
