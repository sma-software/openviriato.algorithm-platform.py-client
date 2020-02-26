import unittest

import AIDMClasses


class AlgorithmTrain(unittest.TestCase):

    def test_train_path_node_objects(self):
        train_path_node = dict(ID=8113, SectionTrackID=None, NodeID=7, NodeTrackID=8, FormationID=1187,
                               ArrivalTime="2003-09-01T00:10:00",
                               DepartureTime="2003-09-01T00:10:00", MinimumRunTime=None, MinimumStopTime="P0D",
                               StopStatus="commercialStop", SequenceNumber=0)
        test_train_path_node = AIDMClasses.TrainPathNode(train_path_node)
        key: str
        for key in train_path_node.keys():
            self.assertEqual(train_path_node[key], getattr(test_train_path_node, key))
            print(key)
            print(getattr(test_train_path_node, key))


