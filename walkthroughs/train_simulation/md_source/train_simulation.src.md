# Train Simulation Walkthrough
This walkthrough demonstrates how the Viriato train simulation can be used and how to implement an own dispatching strategy.

To have a good understanding of this walkthrough, it is recommended that
* you are familiar with the concepts presented in [Walkthrough Creating an Algorithm Using the py_client](@py_client_root/walkthroughs/py_client_usage/dist/py_client_usage.md).
* have read the article from Chapter _Train Simulation_ in the documentation provided with the Algorithm Research SDK.

## Overview

In this article, we are going to implement three different version of a dispatching strategy - referred to as dispatchers in the following - in order to outline the functionality as well as suggest ways of usages.

* We will start with a simple dispatcher prioritising events according to their chronological order.
* We will provide an extension of the first dispatcher to demonstrate how to change the order of two trains in a station where they have a planned stop, leading to a second dispatcher.
* The last dispatcher will show you how to add unplanned stops and then to use these stops to change the order of the trains, which is a natural extension of the second dispatcher.

## The Working Example

Throughout our example, we will use the following sample data to explain how the algorithm works and illustrate the different strategies.

We have two trains:
* First train: travelling between Zurich Flughafen to Zurich Hardbrücke.
* Second train: travelling between Zurich Affoltern to Zurich Hardbrücke.

Both trains share the following nodes on their route
* Zurich Oerlikon
* Hard
* Zurich Hardbrücke

Therefore, if the preceding train is delayed a conflict can occur between the two trains, see Figure 2.

![Conflicting situation](@images/conflicting_scenario.PNG)

_Figure 2: Example of a conflicting situation occurring during the simulation._

In the following we will give different examples, how you can implement your own dispatcher to resolve such conflicts using different methods available on the Algorithm Interface.

## The Glue Code

### Parameters

The presented algorithms request the following parameters:

* The simulation will run in a given time window.
* The user can choose the dispatcher he wants to use to solve conflicts.
* The user can optionally enter two trains of the given scenario. The algorithm will change the order of these trains.

![Parameters](@images/parameters.PNG)

_Figure 3: The user chooses a time window to run the simulation on and if desired the order of two conflicting trains can be changed by selecting the two concerned trains._

### Simulation
First, the simulation has to be started in a time window by the algorithm developer and in our example this time window is given by the user. This loads the timetable data in the given time window for the trains stemming from the reference scenario 
with which the Algorithm Platform has been started. Recall, that for each train path node from each of these trains either two event, one arrival and one departure event, 
or one passing event is created for the simulation. 

@Import(walkthroughs/train_simulation/py/train_simulation_example_runner.py,start_simulation,Starting a simulation in a given time window)

We can retrieve the first executable [AlgorithmTrainSimulationEvent](@py_client_root/algorithm_interface/aidm/aidm_train_simulation_classes.py) from the Algorithm Interface by using the method 
@ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,get_next_train_simulation_event). 

For each event we retrieve a [dispatcher](#Dispatchers) has to decide if they want to realise it using @ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,realize_next_train_simulation_event)
or to postpone it using @ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,postpone_next_train_simulation_event). After making the decision we will be provided the next executable event, 
which is an instance of the type [AlgorithmTrainSimulationRealizationForecast](@py_client_root/algorithm_interface/aidm/aidm_train_simulation_classes.py). The objects of this class contain also all events that had to be postponed by the simulator in order to avoid conflicts. Finally, 
after all events have been realised the simulation terminates.

@Import(walkthroughs/train_simulation/py/train_simulation_example_runner.py,main_loop_controlling_simulation,Main loop to control the simulation)

## Dispatchers
A dispatcher makes for each step of the simulation a decision of what to do with an event. We use an abstract class with a method 
@ImportInlineShort(walkthroughs/train_simulation/py/dispatchers.py,make_decision_for_event) respecting the following structure. This allows us to implement 
different dispatchers and to switch easily between them. 
@Import(walkthroughs/train_simulation/py/dispatchers.py,dispatchers_structure,Structure of the dispatchers)

### Simple dispatcher
The first dispatcher will just realise the events in a first-come first-served manner. In other words, it gives priority to the trains arriving or departing first and 
lets the simulator solve conflicts by delaying a following events if a conflict would occur otherwise, i.e. to avoid conflicts.

@Import(walkthroughs/train_simulation/py/dispatchers.py,SimpleDispatcher,Simple dispatcher)

This strategy can be illustrated with the example presented in Figure 3. Here, the conflict has been solved by adding additional running time to the succeeding 
train between Zurich Seebach and Zurich Oerlikon. The headway time is then respected. 

![Conflict solved by the simple dispatcher](@images/first_in_first_out_dispatcher.PNG)

_Figure 3: Visualisation of the simple dispatcher strategy._

### Order Changing dispatcher
Let us now see how the order of two trains in their first common node can be changed. We extend the planned stop of the preceding train using 
@ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,postpone_next_train_simulation_event) on the departure event of the first common 
node of the two selected trains.

@Import(walkthroughs/train_simulation/py/dispatchers.py,ChangeTrainOrderInFirstCommonTrainPathNodeDispatcher,Dispatcher changing the train order)


For sake of simplicity we have chosen to postpone the departure one minute after the current forecast on the departure of the previously succeeding train, changing the order of the two trains through this. For further details, refert to @ImportInlineShort(walkthroughs/train_simulation/py/dispatcher_service.py,_calculate_time_to_postpone_to)

@Import(walkthroughs/train_simulation/py/dispatcher_service.py,postpone_departure_in_given_node_of_preceding_train_or_realize_event,Example of a dispatcher changing the order of two trains by postponing the departure of the preceding train)

### Dispatcher Adding a Stop to Change the Order of Passing Trains
If a train doesn't have a planned stop and the dispatching strategy still wants to delay the departure on the first common node, there is the possibility to add an unplanned stop by using the 
method @ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,replace_next_train_simulation_event_by_stop). This method will replace a passing 
event by an arrival and a departure event. The latter can then be postponed in the same way as the dispatcher presented just above.

@Import(walkthroughs/train_simulation/py/dispatchers.py,ChangeTrainOrderInFirstCommonTrainPathNodeAddingAStopDispatcher,Dispatcher adding an extra stop)

The strategy of this dispatcher is illustrated in Figure 4. An unplanned stop has been introduced and the departure of this train is one minute after the end
of the conflict between the two trains.

![Conflict solved adding an extra stop and changing the train order](@images/change_train_order_dispatcher.PNG)

_Figure 4: Visualisation of the solution given by the proposed dispatcher changing the order and adding an extra stop._

## Writing Back the Realized Train Runs
In order to analyse and visualize the simulation, we show a method how to persist the realised train runs. For this, it is necessary to iterate over all the train path nodes and update the 
arrival time, departure time and the stop status if an unplanned stop has been introduced during the simulation. We write back the updates through method
@ImportInlineShort(py_client/algorithm_interface/algorithm_interface.py,update_train_times) of the Algorithm Interface. The changed trains can then be saved to a regular Viriato train scenario, persisting the realised train runs. 
The user can visualize them in all Viriato views.

@Import(walkthroughs/train_simulation/py/train_simulation_example_runner.py,persisting_updated_trains,Writing back the result of the simulation)

## Conclusion
Throughout this walkthrough we have presented how to create a simulation for a given scenario using the Algorithm Interface and how to implement different dispatching 
strategies by adding an unplanned stop and extending a stop to resolve conflicts. The presented examples only delay departure events. It is of course possible to 
postpone arrival events in an analogous way.


