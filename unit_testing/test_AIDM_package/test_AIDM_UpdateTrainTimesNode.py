import datetime
import unittest

from AIDMClasses import AIDM_classes


class TestUpdateTrainTimesNode(unittest.TestCase):

    def test_update_train_times_node_object_init_and_attributes(self):
        node_id = 15
        arrival_time = datetime.datetime(2, 2, 2, 2, 2)
        departure_time = datetime.datetime(3, 2, 1, 2, 3)

        test_node = AIDM_classes.updateTrainTimesNode(TrainPathNodeId=node_id, ArrivalTime=arrival_time,
                                                      DepartureTime=departure_time)

        self.assertIsInstance(test_node, AIDM_classes.updateTrainTimesNode)
        self.assertEqual(test_node.TrainPathNodeId, 15)
        self.assertEqual(test_node.ArrivalTime, datetime.datetime(2, 2, 2, 2, 2))
        self.assertEqual(test_node.DepartureTime, datetime.datetime(3, 2, 1, 2, 3))
