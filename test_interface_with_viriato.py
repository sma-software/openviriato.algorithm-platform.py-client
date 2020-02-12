"""
A test script that requires an REST-API of the VIRIATO-Algorithm Platform
"""

import AlgorithmPlatformPyClient as interface_module
import AlgorithmClasses
import AlgorithmStatic


def test_object_initialisation(url_str='http://localhost:8080') -> None:
    # test for the object creation:
    # fails on purpose:
    try:
        url_nr = 952022
        interface_to_viriato = interface_module.AlgorithmicPlatformInterface(url_nr)
        print('was able to insert int as url')  # if we made it here, there is something wrong
        raise NotImplementedError
    except AssertionError:
        print('failed to insert int as url')
    # create an interface with the url as str
    interface_to_viriato = interface_module.AlgorithmicPlatformInterface(url_str)
    print('test_object_initialisation complete')
    return interface_to_viriato


def test_user_notifications(interface_to_viriato) -> None:
    # test user notifications:
    interface_to_viriato.notify_user('hi', 'it works')
    try:
        for i in range(5):
            interface_to_viriato.show_status_message(i)
        print('was able to insert int as show_status_message')
        raise NotImplementedError
    except AssertionError:
        print('failed correctly to insert int as show_status_message')
        # create an interface with the url as str
        interface_to_viriato.show_status_message('Foo', 'bar')
        interface_to_viriato.show_status_message('Foo bar')
    print('test_user_notifications complete')


def test_get_directed_section_tracks(interface_to_viriato) -> None:
    # lets test the robustness:
    for i in range(1, 50):
        for j in range(1, 50):
            if i == j:
                continue
            try:
                directed_section_tracks = interface_to_viriato.get_directed_section_tracks(i, j)
                # if len(directed_section_tracks) > 0:
                # print(directed_section_tracks)
                # for idx in range(len(directed_section_tracks)):
                #    print(directed_section_tracks[idx].ID)
            except AlgorithmStatic.AlgorithmPlatformError:
                i
    print('test_get_directed_section_tracks complete')


def test_get_node_and_get_neighbor_nodes(interface_to_viriato) -> None:
    # lets test the get_node:
    for i in range(1, 100):
        try:
            node_obj = interface_to_viriato.get_node(i)
            node_list = interface_to_viriato.get_neighbor_nodes(i)
        except AlgorithmStatic.AlgorithmPlatformError:
            i
    print('test_get_node_and_get_neighbor_nodes complete')


def test_get_parallel_section_tracks(interface_to_viriato) -> None:
    for i in range(1, 1000):
        try:
            track_list = interface_to_viriato.get_parallel_section_tracks(i)
            # if len(track_list) > 0:
            #    for idx in range(len(track_list)):
            #       print(track_list[idx].ID)
        except AlgorithmStatic.AlgorithmPlatformError:
            i
    print('test_get_parallel_section_tracks complete')


def test_algorithm_node_object(node_id=1, code_string='someTestNodeID', debug_string='', node_tracks=[]):
    test_node = AlgorithmClasses.AlgorithmNode(node_id, code_string, debug_string, node_tracks)
    print(test_node.ID)
    print(test_node.DebugString)
    print(test_node.Code)


def test_train_cancellations(interface_to_viriato: interface_module.AlgorithmicPlatformInterface) -> None:
    for i in range(500, 1000):
        try:
            interface_to_viriato.cancel_train_to(train_path_node_id=i)
        except AlgorithmStatic.AlgorithmPlatformError:
            i
    for i in range(500, 1000):
        try:
            obj = interface_to_viriato.cancel_train_from(train_path_node_id=i)
        except AlgorithmStatic.AlgorithmPlatformError:
            i


def main():
    url_str = 'http://localhost:8080'
    interface_to_viriato: interface_module.AlgorithmicPlatformInterface

    test_object_initialisation(url_str)

    with interface_module.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
        # try to retrieve the url:
        print(interface_to_viriato.base_url)
        print('url retrieve test complete')
        test_user_notifications(interface_to_viriato)
        try:
            print(interface_to_viriato.get_train_classifications())
        except AlgorithmStatic.AlgorithmPlatformError:
            print('Train classifications not configured')

    with test_object_initialisation(url_str) as interface_to_viriato:
        test_get_parallel_section_tracks(interface_to_viriato)
        test_get_directed_section_tracks(interface_to_viriato)

    with interface_module.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
        test_get_node_and_get_neighbor_nodes(interface_to_viriato)

    with interface_module.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
        test_train_cancellations(interface_to_viriato)

    # other tests for the data types
    test_algorithm_node_object(node_id=1, code_string='TestNodeID', debug_string='test_node', node_tracks=['A', 'B'])
    UpdateTrainTimesNode = AlgorithmClasses.UpdateTrainTimesNode


if __name__ == '__main__':
    main()
