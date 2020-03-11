import AlgorithmInterface.AlgorithmInterfaceFactory
import datetime
from AIDMClasses import AIDM_classes

BASE_URL = 'http://localhost:8080'
TRAIN_PATH_NODE_ID=1332
ARRIVAL_TIME=datetime.datetime(2003, 5, 1, 0, 4)
DEPARTURE_TIME=datetime.datetime(2003, 5, 1, 0, 5)

update_train_time_nodes = [AIDM_classes.updateTrainTimesNode(TrainPathNodeId=TRAIN_PATH_NODE_ID,
                                                             ArrivalTime=ARRIVAL_TIME,
                                                             DepartureTime=DEPARTURE_TIME)

with AlgorithmInterface.AlgorithmInterfaceFactory.create(BASE_URL) as algorithm_interface:
    algorithm_interface.
