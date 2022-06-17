
# Rerouting a Train

In this walkthrough we will show how to reroute a train. The scope of this article is only to show how a train can be rerouted on a technical level.
For more detailed information we refer the developer to the C# API Documentation Chapter _Routing Edges and Routes_, which is part of the documentation provided with the Algorithm Research Package.

## The Method for Rerouting Trains

In order to reroute a train, which is possible with the method [reroute_train](../../../py_client/algorithm_interface/algorithm_interface.py), 
the developer has to use the class [UpdateTrainRoute](../../../py_client/aidm/aidm_update_classes.py).

For our walkthrough we have encapsulated the call to [RerouteTrain](../../../py_client/aidm/aidm_update_classes.py) by a method 
`persist_rerouted_train(self, train_to_reroute: AlgorithmTrain, first_train_path_node_on_diversion: AlgorithmTrainPathNode, last_train_path_node_on_diversion: AlgorithmTrainPathNode, routing_edges_on_diversion: List[_RoutingEdge], restore_node_tracks_at_start_and_end_of_diversion: bool) -> AlgorithmTrain`,
which we can simply invoke below. This also demonstrates how an algorithm developer can use [reroute_train](../../../py_client/algorithm_interface/algorithm_interface.py).
Here we list the source code with explanations.

@Import(RerouteTrainPersistenceService,RerouteTrainPersistenceService.py,RerouteTrainPersistenceService source code)

## Picking a Route

For ease of presentation we will select a route in a trivial way. We propose to the developer to use the linked [algorithms.json](../source/algorithms.json). It is not guaranteed that the sample algorithm finds a route, which is valid in the sense that the train can actually run on the given path 
according to the infrastructure context of the Algorithm Platform. The task of computing a valid and good diversion for real use cases is up to the algorithmic expert. For example, you can build up a 
graph datastructure to model the network infrastructure using the methods in Section _Infrastructure_ of the C# API Documentation and find a shortest path using Dijkstra's algorithm on this graph. 

For our example we are given two trains defined by the user. The _train_to_route_ is the train we want to reroute. The alternative route we want to set is defined by the train _train_with_alternative_route_. The user has the responsibility to pick the train with
the alternative route correctly, i.e. to ensure the picked train has the following properties 
* _train_with_alternative_route_ has at least two train path nodes
* the _train_to_reroute_ contains the first node on the path of _train_with_alternative_route_ and it contains the last node on the path of _train_with_alternative_route
* the first occurence of the first node on the path of _train_with_alternative_route_ must be before the last occurence of the last node on the path of _train_with_alternative_route_ on the path of _train_to_reroute_
* it starts and ends at a station

If one of these prerequisites is not met the algorithm will fail. The following code checks if the requirements to the given trains are met and determines the _first_train_path_node_on_diversion_ and the _last_train_path_node_on_diversion_, which are needed for 
our method call, see the previous section.

@Import(RerouteTrainAlgorithm,RerouteTrainAlgorithm.py,RerouteTrainAlgorithm source code)

Continuation of the example below


In a second step we can calculate a sequence of [RoutingEdge](../../../py_client/aidm/aidm_routing_edge_classes.py). Even though the created routing edges might not exist according to the infrastructure, which is known to 
the Algorithm Platform, i.e. these will not be provided by any of the methods [GetOutgoingRoutingEdges](../../../py_client/algorithm_interface/algorithm_interface.py), 
[GetIncomingRoutingEdges](../../../py_client/algorithm_interface/algorithm_interface.py) and 
[GetCrossingRoutingEdges](../../../py_client/algorithm_interface/algorithm_interface.py), we can use them to reroute the train. 

@Import(RerouteTrainAlgorithm3,RerouteTrainAlgorithm.py,Method used to calculate the sequence of routing edges to reroute a train)

Now we can continue with the code from the method above (see comment in the source code listing). We construct the routing edges and we can invoke `persist_rerouted_train(...)` with the obtained routing edges.

Continued example from above

@Import(RerouteTrainAlgorithm2,RerouteTrainAlgorithm.py,Continuation of the RerouteTrainAlgorithm source code)
