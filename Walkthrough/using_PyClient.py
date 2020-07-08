from py_client import *
from py_client.algorithm_interface import algorithm_interface_factory

BASE_URL = 'http://localhost:8080'
from_time = datetime.datetime(year=2003, month=5, day=1, hour=0, minute=0, second=0)
to_time = datetime.datetime(year=2003, month=5, day=10, hour=0, minute=0, second=0)
time_window = TimeWindow(from_time=from_time, to_time=to_time)

with algorithm_interface_factory.create(BASE_URL) as algorithm_interface:
    node_track_closures = algorithm_interface.get_node_track_closures(time_window)
    print("node_track_id: " + str(node_track_closures[0].node_id))
    print("from_time: " + str(node_track_closures[0].closure_time_window.from_time))
    print("to_time: " + str(node_track_closures[0].closure_time_window.to_time))

"""
Expected Example Output:
node_track_id: 622
from_time: datetime.datetime(2003, 5, 1, 0, 0)
to_time: datetime.datetime(2003, 5, 10, 0, 0)
"""