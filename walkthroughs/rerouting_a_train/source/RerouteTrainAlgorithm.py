from typing import List

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.aidm import AlgorithmNode, AlgorithmTrain
from py_client.aidm.aidm_routing_edge_classes import _RoutingEdge, CrossingRoutingEdge, IncomingNodeTrackRoutingEdge, OutgoingNodeTrackRoutingEdge

from RerouteTrainPersistenceService import RerouteTrainPersistenceService


#@RerouteTrainAlgorithm[:74]
class RerouteTrainAlgorithm:
    def run(self, algorithm_interface: AlgorithmInterface):
        # AlgorithmTrain received from interface.
        train_to_reroute = algorithm_interface.get_algorithm_train_parameter("trainToReroute")

        # AlgorithmTrain from which we want to take over a sequence of nodes
        train_with_alternative_route = algorithm_interface.get_algorithm_train_parameter("trainWithAlternativeRoute")

        # check if prerequisites satisfied

        # train with alternative route has at least two train path nodes
        if len(train_with_alternative_route.train_path_nodes) < 2:
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "Train with alternative route ({0}) must have at least two train path nodes. Algorithm aborted. ".format(
                    train_with_alternative_route.debug_string))
            return

        # first and last node of train with alternative route already occur in the train path of the train to reroute.
        first_train_path_node_on_train_with_alternative_path = train_with_alternative_route.train_path_nodes[0]
        last_train_path_node_on_train_with_alternative_path = train_with_alternative_route.train_path_nodes[-1]

        first_train_path_node_on_diversion = [tpn
                                              for tpn in train_to_reroute.train_path_nodes
                                              if tpn.node_id == first_train_path_node_on_train_with_alternative_path.node_id]

        if len(first_train_path_node_on_diversion) == 0:
            start_of_diversion_node = algorithm_interface.get_node(first_train_path_node_on_train_with_alternative_path.node_id)
            algorithm_interface.notify_user("Algorithm Failed",
                                            "Node {0} (ID: {1}) does not exist on train to reroute ({2}). Algorithm aborted. ".format(
                                                                            start_of_diversion_node.Code,
                                                                            start_of_diversion_node.ID,
                                                                            start_of_diversion_node.DebugString))
            return
        first_train_path_node_on_diversion = first_train_path_node_on_diversion[0]

        last_train_path_node_on_diversion = [tpn
                                             for tpn in train_to_reroute.train_path_nodes
                                             if tpn.node_id == last_train_path_node_on_train_with_alternative_path.node_id]
        if len(last_train_path_node_on_diversion) == 0:
            end_of_diversion_node = algorithm_interface.get_node(last_train_path_node_on_train_with_alternative_path.node_id)
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "Node {0} (ID: {1}) does not exist on train to reroute ({2}). Algorithm aborted. ".format(end_of_diversion_node.Code, end_of_diversion_node.ID, end_of_diversion_node.DebugString))
            return
        last_train_path_node_on_diversion = last_train_path_node_on_diversion[-1]

        # firstTrainPathNodeOnDiversion must occur before lastTrainPathNodeOnDiversion on the trainToReroute
        if first_train_path_node_on_diversion.sequence_number >= last_train_path_node_on_diversion.sequence_number:
            start_of_diversion_node = algorithm_interface.get_node(first_train_path_node_on_train_with_alternative_path.node_id)
            end_of_diversion_node = algorithm_interface.get_node(last_train_path_node_on_train_with_alternative_path.node_id)
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "First occurence of node {0} (ID: {1}) must be before the last occurence of node {2}(ID:{3}) on the path of train to reroute ({4}). Algorithm aborted. ".format(
                    start_of_diversion_node.Code,
                    start_of_diversion_node.ID,
                    end_of_diversion_node.Code,
                    end_of_diversion_node.ID,
                    train_to_reroute.DebugString))

        # firstTrainPathNodeOnDiversion and lastTrainPathNodeOnDiversion are stations
        first_node_on_diversion = algorithm_interface.get_node(first_train_path_node_on_diversion.node_id)
        last_node_on_diversion = algorithm_interface.get_node(last_train_path_node_on_diversion.node_id)

        if not self._is_station(first_node_on_diversion):
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "First node on diversion is a junction. Must be a station.")
            return

        if not self._is_station(last_node_on_diversion):
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "Last node on diversion is a junction. Must be a station.")
            return
        # @RerouteTrainAlgorithm2[:]
        # construct mesoscopic routing edges to reroute the train.
        routing_edges_on_diversion = self._construct_mesoscopic_routing_edges_from_train_with_alternative_route(algorithm_interface, train_with_alternative_route)

        reroute_train_persistence_service = RerouteTrainPersistenceService(algorithm_interface)
        rerouted_train = reroute_train_persistence_service.persist_rerouted_train(train_to_reroute, first_train_path_node_on_diversion, last_train_path_node_on_diversion, routing_edges_on_diversion, True)

        message = "Train successfully rerouted. Train visits now {0} nodes on its path.".format(len(rerouted_train.train_path_nodes))
        algorithm_interface.notify_user("Algorithm succeeded", message)

    # @RerouteTrainAlgorithm3[:]
    def _construct_mesoscopic_routing_edges_from_train_with_alternative_route(self, algorithm_interface: AlgorithmInterface, train_with_alternative_path: AlgorithmTrain) -> List[_RoutingEdge]:
        resulting_routing_edges = []
        train_path_node_pairs = zip(
            train_with_alternative_path.train_path_nodes[:-1],
            train_with_alternative_path.train_path_nodes[1:])

        # construct at a time: outgoing (iff first node in pair is station) or crossing mesoscopic routing edge (iff first node is junction)
        # and incoming edge iff second node is station. This will lead to a valid (contiguous) sequence of routing edges.
        for train_path_node_pair in train_path_node_pairs:
            from_node = algorithm_interface.get_node(train_path_node_pair[0].node_id)
            to_node = algorithm_interface.get_node(train_path_node_pair[1].node_id)
            if self._is_station(from_node):
                selected_node_track_id = train_path_node_pair[0].node_track_id \
                    if train_path_node_pair[0].node_track_id \
                    else from_node.node_tracks[0].id
                resulting_routing_edges.append(
                    OutgoingNodeTrackRoutingEdge(
                        train_path_node_pair[0].node_id,
                        selected_node_track_id,
                        train_path_node_pair[1].section_track_id))
            else:
                resulting_routing_edges.append(
                    CrossingRoutingEdge(
                        train_path_node_pair[0].node_id,
                        train_path_node_pair[0].section_track_id,
                        train_path_node_pair[1].section_track_id))

            if self._is_station(to_node):
                selected_node_track_id = train_path_node_pair[1].node_track_id \
                    if train_path_node_pair[1].node_track_id \
                    else to_node.node_tracks[0].id
                resulting_routing_edges.append(
                    IncomingNodeTrackRoutingEdge(
                        to_node.id,
                        train_path_node_pair[1].section_track_id,
                        selected_node_track_id))

        return resulting_routing_edges

    @staticmethod
    def _is_station(node: AlgorithmNode) -> bool:
        return len(node.node_tracks) > 0
