import unittest

import AIDMClasses


class AlgorithmTrain(unittest.TestCase):
    train_path_nodes = [
        dict(ID=8113, SectionTrackID=None, NodeID=7, NodeTrackID=8, FormationID=1187, ArrivalTime="2003-09-01T00:10:00",
             DepartureTime="2003-09-01T00:10:00", MinimumRunTime=None, MinimumStopTime="P0D",
             StopStatus="commercialStop", SequenceNumber=0),
        dict(ID=8114, SectionTrackID=1175, NodeID=15, NodeTrackID=16, FormationID=None,
             ArrivalTime="2003-09-01T00:14:00", DepartureTime="2003-09-01T00:14:00", MinimumRunTime="PT4M",
             MinimumStopTime="P0D", StopStatus="passing", SequenceNumber=1)]

    def test_algorithm_train_objects(self, train_id=5, debug_string='test', train_path_nodes=train_path_nodes):
        test_train = AIDMClasses.AlgorithmTrain(train_id, debug_string, train_path_nodes)
        self.assertEqual(test_train.ID, train_id)
        self.assertEqual(test_train.DebugString, debug_string)
        self.assertIsInstance(test_train.TrainPathNodes[0], AIDMClasses.TrainPathNode)
        self.assertIsInstance(test_train.TrainPathNodes[1], AIDMClasses.TrainPathNode)

