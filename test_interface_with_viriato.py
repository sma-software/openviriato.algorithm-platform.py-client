'''
A test script that requires an REST-API of the VIRIATO-Algorithm Platform
'''

import AlgorithmPlatformPyClient as interface_module


def test_object_initialisiation(url_str='http://localhost:8080/'):
    # test for the object creation:
    # fails on purpose:
    try:
        url_nr = 952022
        interface_to_viriato = interface_module.AlgorithmicPlatformInterface(url_nr)
        # if we made it here, there is something wrong
        print('was able to insert int as url')
        return []
    except AssertionError:
        print('failed corretly to insert int as url')
        # create an interface with the url as str
        interface_to_viriato = interface_module.AlgorithmicPlatformInterface(url_str)
        return interface_to_viriato


def test_user_notifications(interface_to_viriato):
    # test user notifications:
    interface_to_viriato.notify_user('hi', 'it works')
    print('notify user test complete')
    try:
        for i in range(99):
            interface_to_viriato.show_status_message(i)
        print('was able to insert int as show_status_message')
        return 1
    except AssertionError:
        print('failed correctly to insert int as show_status_message')
        # create an interface with the url as str
        interface_to_viriato.show_status_message('Foo', 'bar')
        interface_to_viriato.show_status_message('Foo bar')
    print('show_status_message test complete')
    return 0


def test_get_directed_section_tracks(interface_to_viriato):
    # lets test the robustness:
    for i in range(1, 100):
        for j in range(1, 100):
            if i == j:
                continue
            api_return = interface_to_viriato.get_directed_section_tracks(i, j)
            if isinstance(api_return, dict):
                print(api_return)

    return 0


def main():
    interface_to_viriato = test_object_initialisiation()
    interface_to_viriato.verbosity = 1  # increase verbosity

    # try to retrieve the url:
    print(interface_to_viriato.retrieve_url_to_port)
    print('url retrive test complete')

    check_int = test_user_notifications(interface_to_viriato)
    if check_int != 0:
        raise

    check_int = test_get_directed_section_tracks(interface_to_viriato)
    if check_int != 0:
        raise
    # this is a depreciated call!
    # test_str = 'parameters/train'
    # response = interface_to_viriato.do_request(test_str, 'GET')
    # print(response.json())
    return 0


if __name__ == '__main__':
    main()
