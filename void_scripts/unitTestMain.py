import unittest
import os
import unit_testing_modules.test_interface_init as test_interface_init
import unit_testing_modules.test_infrastructure_requests as test_infrastructure_requests
import unit_testing_modules.test_notifications as test_notifications


class InitTest(test_interface_init.TestObjectInitialisation):
    pass


class NotificationTest(test_notifications.TestUserNotifications):
    pass


class ShowMessageTest(test_notifications.TestShowStatusMessage):
    pass


class DirectedTrack(test_infrastructure_requests.TestGetDirectedSectionTracks):
    pass


if __name__ == '__main__':

    unittest.main()
    print(os.getcwd())
