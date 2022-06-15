# Test

## Picking a Route


If one of these prerequisites is not met the algorithm will fail. The following code checks if the requirements to the given trains are met and determines the `firstTrainPathNodeOnDiversion` and the `lastTrainPathNodeOnDiversion`, which are needed for 
our method call, see the previous section.

@Import(import_part_of_class,RerouteTrainAlgorithm.py,Part of class imported)

Continuation of the example below


In a second step we can calculate a sequence of [RoutingEdge](../../py_client/aidm/aidm_routing_edge_classes.py). Even though the created routing edges might not exist according to the infrastructure, which is known to 
the Algorithm Platform. 

@Import(import_function,RerouteTrainAlgorithm.py,Function imported)

Now we can continue with the code from the method above (see comment in the source code listing). We construct the routing edges and we can invoke `persist_rerouted_train(...)` with the obtained routing edges.

Continued example from above

# next section