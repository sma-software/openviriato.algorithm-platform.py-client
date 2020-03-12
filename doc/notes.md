# Rest API Wrapper in Python

To do: 
- Implement methods, one with "flat" returned objects first

## Implementation Progress
All Methods according to Documentation of REST-API 

##### Implemented Methods and Tests
* Infrastructure
* Train Classifications
* Notifications
* HeadWays
* Separation Times

##### In Progress:

* Trains
* Assignable Station Tracks

##### Not Implemented

* Routing
* Vehicles
* Running Time Calculations
* Parameters
* Possessions

###### Questions:
> resolved - 
> * what to return, when there is no return? return an empty list, None ...
> * Generate Objects from JSON, ok? is it sufficient to just check the content? -> 
> no we want to have full support for the users, which means we have to implement them cleanly 
> * Update Train Time: Perform update node by node --> 
in the example of the API it seems to be that way? --> Updates with list are possible and required!
>

* What to do with time and datetime? cast them to python types?
* In the API Doc, there are sometimes Bodies with CamelCase and With kebabCase, e.g. 
"trainPathNodeID" and "TrainPathNodeID"

###### Second Review

- No need to check what comes from the platform, no assertions required
- Remove assertions which check data from AlgoPlat!
- Split Test such that in and output are tested independently
- Refactor code and especially the tests


###### First Review Feedback:

Find a way to open a connection only once, user should use interface inside a with statement
the user should use it with a with statement as disposable, we have to make sure that we open the connection only once

Move assertions in one function, 
make assertions in a function --> give hint where it has been, e.g. method & argument name

string assembly with request url outside --> not at every call

some inspiration
https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object

