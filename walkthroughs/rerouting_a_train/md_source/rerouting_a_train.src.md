
# Rerouting a Train

In this walkthrough we will show how to reroute a train. The scope of this article is only to show how a train can be rerouted on a technical level.
For more detailed information we refer the developer to the C# API Documentation Chapter _Routing Edges and Routes_, which is part of the documentation provided with the Algorithm Research SDK.

## The Method for Rerouting Trains

In order to reroute a train, which is possible with the method @ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,reroute_train), 
the developer has to use the class [UpdateTrainRoute](@py_client_root/aidm/aidm_update_classes.py).

For our walkthrough we have encapsulated the call to @ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,reroute_train) by a method 
@ImportInlineLong(walkthroughs/rerouting_a_train/py/RerouteTrainPersistenceService.py,persist_rerouted_train)
which we can simply invoke below. This also demonstrates how an algorithm developer can use @ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,reroute_train).
Here we list the source code with explanations.

@Import(walkthroughs/rerouting_a_train/py/RerouteTrainPersistenceService.py,RerouteTrainPersistenceService,RerouteTrainPersistenceService source code)

## Picking a Route

For ease of presentation we will select a route in a trivial way. We propose to the developer to use the linked [algorithms.json](../config/algorithms.json). It is not guaranteed that the sample algorithm finds a route, which is valid in the sense that the train can actually run on the given path 
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

@Import(walkthroughs/rerouting_a_train/py/RerouteTrainAlgorithm.py,RerouteTrainAlgorithm,RerouteTrainAlgorithm source code. Continuation of the example below.)


In a second step we can calculate a sequence of [RoutingEdge](@py_client_root/aidm/aidm_routing_edge_classes.py). Even though the created routing edges might not exist according to the infrastructure, which is known to 
the Algorithm Platform, i.e. these will not be provided by any of the methods @ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,get_outgoing_routing_edges), 
@ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,get_incoming_routing_edges) and 
@ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,get_crossing_routing_edges), we can use them to reroute the train. 

@Import(walkthroughs/rerouting_a_train/py/RerouteTrainAlgorithm.py,RerouteTrainAlgorithm3,Method used to calculate the sequence of routing edges to reroute a train)

Now we can continue with the code from the method above (see comment in the source code listing). We construct the routing edges and we can invoke @ImportInlineShort(walkthroughs/rerouting_a_train/py/RerouteTrainPersistenceService.py,persist_rerouted_train) with the obtained routing edges.

Continued example from above

@Import(walkthroughs/rerouting_a_train/py/RerouteTrainAlgorithm.py,RerouteTrainAlgorithm2,Continuation of the RerouteTrainAlgorithm source code)
