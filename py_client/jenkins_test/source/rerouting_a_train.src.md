# Test

## Picking a Route


If one of these prerequisites is not met the algorithm will fail. The following code checks if the requirements to the given trains are met and determines the `firstTrainPathNodeOnDiversion` and the `lastTrainPathNodeOnDiversion`, which are needed for 
our method call, see the previous section.

@Import(import_part_of_class,jenkins_tests/source/RerouteTrainAlgorithm.py,Continuation of the example below)


In a second step we can calculate a sequence of [RoutingEdge](@py_client_root/aidm/aidm_routing_edge_classes.py). Even though the created routing edges might not exist according to the infrastructure, which is known to 
the Algorithm Platform. 

@Import(import_function,jenkins_tests/source/RerouteTrainAlgorithm.py,Continued example from above)

Here is a short signature import @ImportInlineShort(jenkins_tests/source/RerouteTrainAlgorithm.py,_construct_mesoscopic_routing_edges_from_train_with_alternative_route) and a long import signature from the py_client root @ImportInlineLong(jenkins_tests/source/RerouteTrainAlgorithm.py,_construct_mesoscopic_routing_edges_from_train_with_alternative_route)

# next section