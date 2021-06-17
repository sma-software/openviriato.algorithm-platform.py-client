![#openviriato logo](openviriato_400px.png)

# openviriato.algorithm-platform.py-client

## The Pythonic API Wrapper for Viriato's Algorithm Platform

We provide a Python client implementing the [AlgorithmInterface](py_client/algorithm_interface/algorithm_interface.py) in Python. If you want to implement your algorithms with Python you can use this client instead of working with the REST interface directly. It offers type-hints and takes over all low-level functionality needed like object serialization of Python objects to JSON objects and deserialization in the other direction such that you can immediately start working. In this case, the relevant API for you is directly our Python API. Under the hood, the communication with the Algorithm Platform is still carried out via REST calls and your algorithms run in a separate process. The only thing you have to do is to install the wheel file shipped with the Algorithm Platform SDK in your Python environment, see below.

## Getting Started

We refer the reader to the [Walkthrough using the py_client](Walkthrough/py_client_usage_walkthrough.md) to see how the py_client can be used by an algorithm.

