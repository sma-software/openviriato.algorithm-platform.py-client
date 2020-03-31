"""
A test script that requires an REST-API of the VIRIATO-Algorithm Platform
"""
import AlgorithmInterface.AlgorithmInterface
import Communication.ResponseProcessing
from Communication import CommunicationLayer


def test_object_initialisation(url_str='http://localhost:8080') -> \
        AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface:
    # test for the object creation:
    # fails on purpose:
    try:
        url_nr = 952022
        interface_to_viriato = AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(url_nr)
        print('was able to insert int as url')  # if we made it here, there is something wrong
        raise NotImplementedError
    except AssertionError:
        print('failed to insert int as url')
    # create an interface with the url as str
    interface_to_viriato = AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(url_str)
    print('test_object_initialisation complete')
    return interface_to_viriato


def test_user_notifications(interface_to_viriato) -> None:
    # test user notifications:
    interface_to_viriato.notify_user('hi', 'it works')
    interface_to_viriato.show_status_message('Foo', 'bar')
    interface_to_viriato.show_status_message('Foo bar')


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
            except Communication.ResponseProcessing.AlgorithmPlatformError:
                pass
    print('test_get_directed_section_tracks complete')


def test_get_node_and_get_neighbor_nodes(interface_to_viriato) -> None:
    # lets test the get_node:
    for i in range(1, 100):
        try:
            node_obj = interface_to_viriato.get_node(i)
            node_list = interface_to_viriato.get_neighbor_nodes(i)
        except Communication.ResponseProcessing.AlgorithmPlatformError:
            pass
    print('test_get_node_and_get_neighbor_nodes complete')


def test_get_parallel_section_tracks(interface_to_viriato) -> None:
    for i in range(1, 1000):
        try:
            track_list = interface_to_viriato.get_parallel_section_tracks(i)
            # if len(track_list) > 0:
            #    for idx in range(len(track_list)):
            #       print(track_list[idx].ID)
        except Communication.ResponseProcessing.AlgorithmPlatformError:
            pass
    print('test_get_parallel_section_tracks complete')


def test_train_cancellations(
        interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface) -> None:
    for i in range(500, 2500):
        try:
            obj = interface_to_viriato.cancel_train_to(train_path_node_id=i)
            print(vars(obj))
        except Communication.ResponseProcessing.AlgorithmPlatformError:
            pass
    for i in range(500, 2500):
        try:
            obj = interface_to_viriato.cancel_train_from(train_path_node_id=i)
            print(vars(obj))
        except Communication.ResponseProcessing.AlgorithmPlatformError:
            pass


def main():
    url_str = 'http://localhost:8080'
    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
        test_train_cancellations(interface_to_viriato)
        print('test_train_cancellations complete')

    with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
        # try to retrieve the url:
        print(interface_to_viriato.base_url)
        print('url retrieve test complete')
        test_user_notifications(interface_to_viriato)
        try:
            print(interface_to_viriato.get_train_classifications())
        except Communication.ResponseProcessing.AlgorithmPlatformError:
            print('Train classifications not configured')

    with test_object_initialisation(url_str) as interface_to_viriato:
        test_get_parallel_section_tracks(interface_to_viriato)
        test_get_directed_section_tracks(interface_to_viriato)

    with AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
        test_get_node_and_get_neighbor_nodes(interface_to_viriato)


if __name__ == '__main__':
    main()
