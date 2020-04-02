import datetime

import AIDMClasses.AIDM_TimeWindow_classes
import AlgorithmInterface.AlgorithmInterfaceFactory
from AIDMClasses import AIDM_TrainPathNode_classes

BASE_URL = 'http://localhost:8080'
from_time = datetime.datetime(year=2003, month=5, day=1, hour=0, minute=0, second=0)
to_time = datetime.datetime(year=2003, month=5, day=10, hour=0, minute=0, second=0)
time_window = AIDMClasses.AIDM_TimeWindow_classes.TimeWindow(FromTime=from_time, ToTime=to_time)

with AlgorithmInterface.AlgorithmInterfaceFactory.create(BASE_URL) as algorithm_interface:
    node_track_closures = algorithm_interface.get_node_track_closures(time_window)
    print("NodeTrackID: " + node_track_closures[0].NodeID)
    print("FromTime: " + node_track_closures[0].ClosureTimeWindow.FromTime)
    print("ToTime: " + node_track_closures[0].ClosureTimeWindow.ToTime)

"""
Expected Example Output:
NodeTrackID: 622
FromTime: datetime.datetime(2003, 5, 1, 0, 0)
ToTime: datetime.datetime(2003, 5, 10, 0, 0)
"""