# Test

## Picking a Route


If one of these prerequisites is not met the algorithm will fail. The following code checks if the requirements to the given trains are met and determines the `firstTrainPathNodeOnDiversion` and the `lastTrainPathNodeOnDiversion`, which are needed for 
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
        if (len(train_with_alternative_route.train_path_nodes) < 2) :
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
                                                                            startOfDiversionNode.Code,
                                                                            startOfDiversionNode.ID,
                                                                            trainToReroute.DebugString))
            return
        first_train_path_node_on_diversion = first_train_path_node_on_diversion[0]

        last_train_path_node_on_diversion = [tpn
                                             for tpn in train_to_reroute.train_path_nodes
                                             if tpn.node_id == last_train_path_node_on_train_with_alternative_path.node_id]
        if (len(last_train_path_node_on_diversion) == 0):
            end_of_diversion_node = algorithm_interface.get_node(last_train_path_node_on_train_with_alternative_path.node_id)
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "Node {0} (ID: {1}) does not exist on train to reroute ({2}). Algorithm aborted. ".format(endOfDiversionNode.Code, endOfDiversionNode.ID, trainToReroute.DebugString))
            return
        last_train_path_node_on_diversion = last_train_path_node_on_diversion[-1]

        # firstTrainPathNodeOnDiversion must occur before lastTrainPathNodeOnDiversion on the trainToReroute
        if (first_train_path_node_on_diversion.sequence_number >= last_train_path_node_on_diversion.sequence_number):
            start_of_diversion_node = algorithm_interface.get_node(first_train_path_node_on_train_with_alternative_path.node_id)
            end_of_diversion_node = algorithm_interface.get_node(last_train_path_node_on_train_with_alternative_path.node_id)
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "First occurence of node {0} (ID: {1}) must be before the last occurence of node {2}(ID:{3}) on the path of train to reroute ({4}). Algorithm aborted. ".format(
                    startOfDiversionNode.Code,
                    startOfDiversionNode.ID,
                    endOfDiversionNode.Code,
                    endOfDiversionNode.ID,
                    trainToReroute.DebugString))

        # firstTrainPathNodeOnDiversion and lastTrainPathNodeOnDiversion are stations
        first_node_on_diversion = algorithm_interface.get_node(first_train_path_node_on_diversion.node_id)
        last_node_on_diversion = algorithm_interface.get_node(last_train_path_node_on_diversion.node_id)

        if (not self._is_station(first_node_on_diversion)):
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "First node on diversion is a junction. Must be a station.")
            return

        if (not self._is_station(last_node_on_diversion)):
            algorithm_interface.notify_user(
                "Algorithm Failed",
                "Last node on diversion is a junction. Must be a station.")

```
_Code listing: Part of class imported_. ([_Lines: 11 - 84 from file: RerouteTrainAlgorithm.py_](../source/RerouteTrainAlgorithm.py#L11-L84)).

Continuation of the example below


In a second step we can calculate a sequence of [RoutingEdge](../../../py_client/aidm/aidm_routing_edge_classes.py). Even though the created routing edges might not exist according to the infrastructure, which is known to 
the Algorithm Platform. 

```python
def _is_station(self, node: AlgorithmNode) -> bool:
    return len(node.node_tracks) > 0
```
_Code listing: Function imported_. ([_Lines: 136 - 137 from file: RerouteTrainAlgorithm.py_](../source/RerouteTrainAlgorithm.py#L136-L137)).

Now we can continue with the code from the method above (see comment in the source code listing). We construct the routing edges and we can invoke `persist_rerouted_train(...)` with the obtained routing edges.

Continued example from above

# next section