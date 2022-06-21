# Walkthrough Creating an Algorithm Using the py_client

In this walkthrough we will show you how to create algorithms using the [AlgorithmInterface](../../../py_client/algorithm_interface/algorithm_interface.py) via the Python client (py_client) provided with the Algorithm Platform.
                                                                                        
                                                                         

## Documentation

As the py_client strongly follows the C#-Client combined with Python's coding
conventions (according to [PEP 8]), [see the example below](../source/count_trains_py_client.py)), there is no
dedicated documentation. Instead, we refer the developer to the C# API Documentation Chapter, which is part of the documentation provided with the Algorithm Research Package. 
                                                                  

We also support
Python's type hints showing the developer the correct Python syntax and strongly supporting a rapid development:

![CodeCompletionInPyCharm](../images/code_completion_py_client.png)

## Installing the py_client

There are different ways of working and installing the py_client. We recommend - for each one of your projects - to
install the py_client package into a separate virtual environment at the same directory level as your main script. We
show in the following how to accomplish this assuming Python is in the path.

We proceed in three steps.

* Creating the environment,
* activating it and
* installing the py_client package with the installation tool pip into the virtual environment.

The official Python release provides all needed tools / scripts / modules. Change to a directory where you want
to develop your algorithm. We assume we are in the following directory:

```
${FolderToAlgorithmPlatform}\\Extension\\AlgorithmPlatform\\algorithms
```

The following commands cover the three steps above:

```shell
rem Step 1: create environment
python -m venv demo_venv
rem Step 2: activate environment                                          
demo_venv\Scripts\activate.bat 
rem Step 3: install py_client package and its dependencies copied to same directory previously
pip install sma.algorithm_platform.py_client-{py_client-version}.whl
```

## Counting Trains with the py_client

Having installed the py_client we can start to develop our algorithm. Just import
the [AlgorithmInterface](../../../py_client/algorithm_interface/algorithm_interface.py)
and use it by putting it into a `with` statement. Then you can use all available methods. The example code shows how to
query all [AlgorithmTrain](../../../py_client/aidm/aidm_algorithm_classes.py) in a given [TimeWindow](../../../py_client/aidm/aidm_time_window_classes.py), counts them and sends a message to the user reporting the number. You can [download this sample](../source/count_trains_py_client.py).

```python
import argparse
from py_client.algorithm_interface import algorithm_interface_factory


def count_trains_in_time_window(api_url: str):
    with algorithm_interface_factory.create(api_url) as algorithm_interface:
        time_window = algorithm_interface.get_time_window_algorithm_parameter("timeWindowParameter")
        trains_in_window = algorithm_interface.get_trains(time_window)

        algorithm_interface.notify_user(
            "count_trains_algorithm",
            "Found {0} trains in time window from {1} to {2}".format(
                len(trains_in_window),
                time_window.from_time,
                time_window.to_time))


def parse_api_url_from_command_line_arguments() -> str:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-u", "--api_url", required=True)
    command_line_arguments = vars(argument_parser.parse_args())
    api_url: str = command_line_arguments["api_url"]
    return api_url


def main():
    api_url = parse_api_url_from_command_line_arguments()
    count_trains_in_time_window(api_url=api_url)


if __name__ == '__main__':
    main()

```
_Code listing: count_trains_py_client source code_. ([_Lines: 2 - 33 from file: walkthroughs/py_client_usage/source/count_trains_py_client.py_](../../../walkthroughs/py_client_usage/source/count_trains_py_client.py#L2-L33)).

## Configuration for the Deployment

See the chapter '_Deployment and Parameter Passing_' in the official Algorithm Platform documentation for how to deploy an
algorithm. Here, we give a sample configuration to make our algorithm run, assuming we have set up the
environment `demo_env` as described in the [previous paragraph](#installing-the-py_client) and
that the algorithm is saved under

```
${FolderToAlgorithmPlatform}\\Extension\\AlgorithmPlatform\\algorithms\\count_trains_py_client.py
```
Then we may save the algorithm configuration in the `algorithms.json`:

```json
{
  "name": "Count Trains in time window (py_client)",
  "startupRestInterfaceOnly": false,
  "parameterDescriptions": [
    {
      "key": "timeWindowParameter",
      "label": "Time Window Parameter",
      "type": "TimeWindow",
      "tooltip": "Defines the time-window to count the trains in."
    }
  ],
  "workingDirectory": "../algorithms",
  "files": [
    "count_trains_py_client.py"
  ],
  "command": "demo_venv\\Scripts\\python.exe",
  "arguments": "{File[0]} -u {ApiUrl}"
}
```