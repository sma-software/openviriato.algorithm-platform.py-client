import unittest
import os
import AlgorithmPlatformPyClient
import unit_testing_modules.test_interface_init as test_interface_init
import unit_testing_modules.test_infrastructure_requests as test_infrastructure_requests
import unit_testing_modules.test_nofifcations as test_nofifcations


class InitTest(test_interface_init.TestObjectInitialisation):
    pass


class NotificationTest(test_nofifcations.TestUserNotifications):
    pass


class ShowMessageTest(test_nofifcations.TestShowStatusMessage):
    pass


class DirectedTrack(test_infrastructure_requests.TestGetDirectedSectionTracks):
    pass


if __name__ == '__main__':
    unittest.TestLoader.discover(start_dir=os.getcwd().join('unit_testing_modules'))
    unittest.main()
