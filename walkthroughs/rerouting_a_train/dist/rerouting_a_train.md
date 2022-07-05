
# Rerouting a Train

In this walkthrough we will show how to reroute a train. The scope of this article is only to show how a train can be rerouted on a technical level.
For more detailed information we refer the developer to the C# API Documentation Chapter _Routing Edges and Routes_, which is part of the documentation provided with the Algorithm Research SDK.

## The Method for Rerouting Trains

In order to reroute a train, which is possible with the method [reroute_train(...)](../../../py_client/algorithm_interface/algorithm_interface.py#L289), 
the developer has to use the class [UpdateTrainRoute](../../../py_client/aidm/aidm_update_classes.py).

For our walkthrough we have encapsulated the call to [reroute_train(...)](../../../py_client/algorithm_interface/algorithm_interface.py#L289) by a method 
[persist_rerouted_train(self, train_to_reroute: AlgorithmTrain, first_train_path_node_on_diversion: AlgorithmTrainPathNode, last_train_path_node_on_diversion: AlgorithmTrainPathNode, routing_edges_on_diversion: List[_RoutingEdge], restore_node_tracks_at_start_and_end_of_diversion: bool) -> AlgorithmTrain](../../../walkthroughs/rerouting_a_train/source/RerouteTrainPersistenceService.py#L14)
which we can simply invoke below. This also demonstrates how an algorithm developer can use [reroute_train(...)](../../../py_client/algorithm_interface/algorithm_interface.py#L289).
Here we list the source code with explanations.

```python
from typing import List
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.aidm import AlgorithmTrain, AlgorithmTrainPathNode, UpdateTrainRoute
from py_client.aidm.aidm_routing_edge_classes import _RoutingEdge


class RerouteTrainPersistenceService:
    _algorithm_interface: AlgorithmInterface

    def __init__(self, algorithm_interface: AlgorithmInterface):
        self._algorithm_interface = algorithm_interface

    def persist_rerouted_train(self, train_to_reroute: AlgorithmTrain, first_train_path_node_on_diversion: AlgorithmTrainPathNode, last_train_path_node_on_diversion: AlgorithmTrainPathNode, routing_edges_on_diversion: List[_RoutingEdge], restore_node_tracks_at_start_and_end_of_diversion: bool) -> AlgorithmTrain:
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

        if restore_node_tracks_at_start_and_end_of_diversion:
            self._algorithm_interface.update_node_track(train_to_reroute.id, first_train_path_node_on_diversion.id, first_train_path_node_on_diversion.node_track_id)
            self._algorithm_interface.update_node_track(train_to_reroute.id, last_train_path_node_on_diversion.id, last_train_path_node_on_diversion.node_track_id)

        return rerouted_train

```
Code listing: _RerouteTrainPersistenceService source code_. ([Lines: 2 - 33 from file: _RerouteTrainPersistenceService.py_](../../../walkthroughs/rerouting_a_train/source/RerouteTrainPersistenceService.py#L2-L33)).

## Picking a Route

For ease of presentation we will select a route in a trivial way. We propose to the developer to use the linked [algorithms.json](../source/algorithms.json). It is not guaranteed that the sample algorithm finds a route, which is valid in the sense that the train can actually run on the given path 
according to the infrastructure context of the Algorithm Platform. The task of computing a valid and good diversion for real use cases is up to the algorithmic expert. For example, you can build up a 
graph data structure to model the network infrastructure using the methods in Section _Infrastructure_ of the documentation provided with the Algorithm Research SDK and find a shortest path using Dijkstra's algorithm on this graph. 

For our example we are given two trains defined by the user. The _train_to_route_ is the train we want to reroute. The alternative route we want to set is defined by the train _train_with_alternative_route_. The user has the responsibility to pick the train with
the alternative route correctly, i.e. to ensure the picked train has the following properties 
* _train_with_alternative_route_ has at least two train path nodes
* the _train_to_reroute_ contains the first node on the path of _train_with_alternative_route_ and it contains the last node on the path of _train_with_alternative_route_
* the first occurrence of the first node on the path of _train_with_alternative_route_ must be before the last occurrence of the last node on the path of _train_with_alternative_route_ on the path of _train_to_reroute_
* it starts and ends at a station

If one of these prerequisites is not met the algorithm will fail. The following code checks if the requirements to the given trains are met and determines the _first_train_path_node_on_diversion_ and the _last_train_path_node_on_diversion_, which are needed for 
our method call, see the previous section.

```python
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

        # validate that first and last node of train with alternative route already occur in the train path
        # of the train to reroute.
        first_train_path_node_on_train_with_alternative_path = train_with_alternative_route.train_path_nodes[0]
        last_train_path_node_on_train_with_alternative_path = train_with_alternative_route.train_path_nodes[-1]

        train_to_reroute_contains_first_node_on_diversion = \
            first_train_path_node_on_train_with_alternative_path.node_id in [train_path_node.node_id
                                                                             for train_path_node
                                                                             in train_to_reroute.train_path_nodes]
        if not train_to_reroute_contains_first_node_on_diversion:
            start_of_diversion_node = algorithm_interface.get_node(first_train_path_node_on_train_with_alternative_path.node_id)
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "Node {0} (ID: {1}) does not exist on train to reroute ({2}). Algorithm aborted. ".format(
                    start_of_diversion_node.code, start_of_diversion_node.id, start_of_diversion_node.debug_string))
            return

        train_to_reroute_contains_last_node_on_diversion = \
            last_train_path_node_on_train_with_alternative_path.node_id in [train_path_node.node_id
                                                                            for train_path_node
                                                                            in train_to_reroute.train_path_nodes]
        if not train_to_reroute_contains_last_node_on_diversion:
            end_of_diversion_node = algorithm_interface.get_node(last_train_path_node_on_train_with_alternative_path.node_id)
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "Node {0} (ID: {1}) does not exist on train to reroute ({2}). Algorithm aborted. ".format(
                    end_of_diversion_node.code, end_of_diversion_node.id, end_of_diversion_node.debug_string))
            return

        first_train_path_node_on_diversion = [tpn
                                              for tpn in train_to_reroute.train_path_nodes
                                              if tpn.node_id == first_train_path_node_on_train_with_alternative_path.node_id][0]

        last_train_path_node_on_diversion = [tpn
                                             for tpn in train_to_reroute.train_path_nodes
                                             if tpn.node_id == last_train_path_node_on_train_with_alternative_path.node_id][-1]

        # first_train_path_node_on_diversion must occur before last_train_path_node_on_diversion on the train_to_reroute
        if first_train_path_node_on_diversion.sequence_number >= last_train_path_node_on_diversion.sequence_number:
            start_of_diversion_node = algorithm_interface.get_node(first_train_path_node_on_train_with_alternative_path.node_id)
            end_of_diversion_node = algorithm_interface.get_node(last_train_path_node_on_train_with_alternative_path.node_id)
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "First occurence of node {0} (ID: {1}) must be before the last occurence of node {2}(ID:{3}) on the path of train to reroute ({4}). Algorithm aborted. ".format(
                    start_of_diversion_node.code,
                    start_of_diversion_node.id,
                    end_of_diversion_node.code,
                    end_of_diversion_node.id,
                    train_to_reroute.debug_string))

        # first_train_path_node_on_diversion and last_train_path_node_on_diversion are stations
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

```
Code listing: _RerouteTrainAlgorithm source code. Continuation of the example below._. ([Lines: 11 - 92 from file: _RerouteTrainAlgorithm.py_](../../../walkthroughs/rerouting_a_train/source/RerouteTrainAlgorithm.py#L11-L92)).


In a second step we can calculate a sequence of [RoutingEdge](../../../py_client/aidm/aidm_routing_edge_classes.py). Even though the created routing edges might not exist according to the infrastructure, which is known to 
the Algorithm Platform, i.e. these will not be provided by any of the methods [get_outgoing_routing_edges(...)](../../../py_client/algorithm_interface/algorithm_interface.py#L507), 
[get_incoming_routing_edges(...)](../../../py_client/algorithm_interface/algorithm_interface.py#L500) and 
[get_crossing_routing_edges(...)](../../../py_client/algorithm_interface/algorithm_interface.py#L512), we can use them to reroute the train. 

```python
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

```
Code listing: _Method used to calculate the sequence of routing edges to reroute a train_. ([Lines: 106 - 143 from file: _RerouteTrainAlgorithm.py_](../../../walkthroughs/rerouting_a_train/source/RerouteTrainAlgorithm.py#L106-L143)).

Now we can continue with the code from the method above (see comment in the source code listing). We construct the routing edges and we can invoke [persist_rerouted_train(...)](../../../walkthroughs/rerouting_a_train/source/RerouteTrainPersistenceService.py#L14) with the obtained routing edges.

Continued example from above

```python
# construct mesoscopic routing edges to reroute the train.
routing_edges_on_diversion = self._construct_mesoscopic_routing_edges_from_train_with_alternative_route(algorithm_interface, train_with_alternative_route)
reroute_train_persistence_service = RerouteTrainPersistenceService(algorithm_interface)
rerouted_train = reroute_train_persistence_service.persist_rerouted_train(train_to_reroute, first_train_path_node_on_diversion, last_train_path_node_on_diversion, routing_edges_on_diversion, True)
message = "Train successfully rerouted. Train visits now {0} nodes on its path.".format(len(rerouted_train.train_path_nodes))
algorithm_interface.notify_user("Algorithm succeeded", message)

```
Code listing: _Continuation of the RerouteTrainAlgorithm source code_. ([Lines: 96 - 103 from file: _RerouteTrainAlgorithm.py_](../../../walkthroughs/rerouting_a_train/source/RerouteTrainAlgorithm.py#L96-L103)).
