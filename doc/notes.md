# Rest API Wrapper in Python

To do: 
- Enhance test with mock
- Do tests in unit test
- Implement methods

## Implementation Progress
All Methods according to Documentation of REST-API 

##### Implemented Methods
* Infrastructure
* Train Classifications
* Notifications

##### In Progress:

* Trains
* Assignable Station Tracks


##### Not Implemented
* Separation Times
* Headway Times
* Routing
* Vehicles
* Running Time Calculations
* Parameters
* Possessions


###### Questions:
> resolved - what to return, when there is no return? return an empty list, None ...
* Generate Objects from JSON, ok? is it sufficient to just check the content?


###### Firs Review Feedback:

Find a way to open a connection only once, user should use interface inside a with statement
the user should use it with a with statement as disposable, we have to make sure that we open the connection only once

Move assertions in one function, 
make assertions in a function --> give hint where it has been, e.g. method & argument name

string assembly with request url outside --> not at every call

some inspiration
https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object

