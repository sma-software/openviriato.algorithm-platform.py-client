import requests
import AlgorithmPlatformPyClient as interface_module

def main():
    # create an interface with the url
    url_str = 'http://localhost:8080/'
    interface_to_viriato = interface_module.AlgorithmicPlatformInterface(url_str)
    test_str = 'parameters/train'
    # do it
    interface_to_viriato.verbosity = 1
    print(interface_to_viriato.retrieve_url_to_port())
    response = interface_to_viriato.do_request(test_str, 'GET')
    print(response.json())
    interface_to_viriato.notify_user('hi','it works')
    interface_to_viriato.show_status_message('hi','it works')
    for i in range(99):
        interface_to_viriato.show_status_message(i)

if __name__ == '__main__':
    main()
