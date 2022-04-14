from typing import List

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.aidm import AlgorithmTrain, AlgorithmTrainPathNode, UpdateTrainRoute
from py_client.aidm.aidm_routing_edge_classes import _RoutingEdge

class RerouteTrainPersistenceService:
    _algorithm_interface: AlgorithmInterface

    def __init__(self, algorithm_interface: AlgorithmInterface):
        self._algorithm_interface = algorithm_interface

    def persist_rerouted_train(self, train_to_reroute: AlgorithmTrain, first_train_path_node_on_diversion: AlgorithmTrainPathNode, last_train_path_node_on_diversion: AlgorithmTrainPathNode, routing_edges_on_diversion: List[_RoutingEdge], restore_node_tracks_at_start_and_end_of_diversion: bool) -> AlgorithmTrain :
        first_routing_edge = routing_edges_on_diversion[0]
        last_routing_edge = routing_edges_on_diversion[-1]

        # set the node tracks on first and last node of diversion so that train can be rerouted according to the given sequence of
        # mesoscopic routing edges
        self._algorithm_interface.update_node_track(train_to_reroute.id, first_train_path_node_on_diversion.id, first_routing_edge.start_node_track_id)
        self._algorithm_interface.update_node_track(train_to_reroute.id, last_train_path_node_on_diversion.id, last_routing_edge.end_node_track_id)

        # create the update we want to send to AlgorithmPlatform
        update_train_route = UpdateTrainRoute(first_train_path_node_on_diversion.id, last_train_path_node_on_diversion.id, routing_edges_on_diversion)

        # and assign the route to the train, thereby obtaining the rerouted train
        rerouted_train = self._algorithm_interface.reroute_train(train_to_reroute.id, update_train_route)

        if (restore_node_tracks_at_start_and_end_of_diversion):
            self._algorithm_interface.update_node_track(train_to_reroute.id, first_train_path_node_on_diversion.id, first_train_path_node_on_diversion.node_track_id)
            self._algorithm_interface.update_node_track(train_to_reroute.id, last_train_path_node_on_diversion.id, last_train_path_node_on_diversion.node_track_id)

        return  rerouted_train