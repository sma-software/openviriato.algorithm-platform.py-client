"""
A test script that requires an REST-API of the VIRIATO-Algorithm Platform
"""

import AlgorithmPlatformPyClient as interface_module
import AlgorithmClasses
import AlgorithmStatic


def test_object_initialisation(url_str='http://localhost:8080'):
    # test for the object creation:
    # fails on purpose:
    try:
        url_nr = 952022
        interface_to_viriato = interface_module.AlgorithmicPlatformInterface(url_nr)
        # if we made it here, there is something wrong
        print('was able to insert int as url')
        return []
    except AssertionError:
        print('failed to insert int as url')
    # create an interface with the url as str
    interface_to_viriato = interface_module.AlgorithmicPlatformInterface(url_str)
    print('test_object_initialisation complete')
    return interface_to_viriato


def test_user_notifications(interface_to_viriato) -> int:
    # test user notifications:
    interface_to_viriato.notify_user('hi', 'it works')
    try:
        for i in range(5):
            interface_to_viriato.show_status_message(i)
        print('was able to insert int as show_status_message')
        return 1
    except AssertionError:
        print('failed correctly to insert int as show_status_message')
        # create an interface with the url as str
        interface_to_viriato.show_status_message('Foo', 'bar')
        interface_to_viriato.show_status_message('Foo bar')
    print('test_user_notifications complete')


def test_get_directed_section_tracks(interface_to_viriato):
    """
    :return: 0 if passed
    :rtype: int
    :type interface_to_viriato: interface_module.AlgorithmicPlatformInterface
    """
    # lets test the robustness:
    for i in range(1, 50):
        for j in range(1, 50):
            if i == j:
                continue
            try:
                track_info = interface_to_viriato.get_directed_section_tracks(i, j)
                # print(track_info)
            except AlgorithmStatic.AlgorithmPlatformError:
                i
                # print('at least one of the nodes does not exist')
    print('test_get_directed_section_tracks complete')


def test_get_node_and_get_neighbor_nodes(interface_to_viriato):
    """
    :return: 0 if passed
    :rtype: int
    :type interface_to_viriato: interface_module.AlgorithmicPlatformInterface
    """
    # lets test the get_node:
    for i in range(1, 100):
        try:
            node_obj = interface_to_viriato.get_node(i)
            node_list = interface_to_viriato.get_neighbor_nodes(i)
        except AlgorithmStatic.AlgorithmPlatformError:
            i
    print('test_get_node_and_get_neighbor_nodes complete')


def test_get_parallel_section_tracks(interface_to_viriato):
    """
    :return: 0 if passed
    :rtype: int
    :type interface_to_viriato: interface_module.AlgorithmicPlatformInterface
    """
    # lets test the get_node:
    for i in range(250, 501):
        try:
            track_list = interface_to_viriato.get_parallel_section_tracks(i)
            # print(track_list)
        except AlgorithmStatic.AlgorithmPlatformError:
            print()
    print('test_get_parallel_section_tracks complete')


def test_algorithm_node_object():
    test_node = AlgorithmClasses.AlgorithmNode(node_id=1, code_string='someTestNodeID', debug_string='', node_tracks=[])
    print(test_node.ID)
    print(test_node.DebugString)
    print(test_node.Code)


def main():
    url_str = 'http://localhost:8080'
    """
    gathers all tests to check if the client is working as intended. Requires an active Algorithm Platform API
    :return: int 0
    """

    interface_to_viriato: interface_module.AlgorithmicPlatformInterface
    test = 1

    test_object_initialisation()

    with interface_module.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
        # try to retrieve the url:
        print(interface_to_viriato.base_url)
        print('url retrieve test complete')
        test_user_notifications(interface_to_viriato)

    with test_object_initialisation() as interface_to_viriato:
        test_get_parallel_section_tracks(interface_to_viriato)
        test_get_node_and_get_neighbor_nodes(interface_to_viriato)
        test_get_directed_section_tracks(interface_to_viriato)
        test_algorithm_node_object()


if __name__ == '__main__':
    main()
