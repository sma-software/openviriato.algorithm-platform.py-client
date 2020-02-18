"""
This is a script intended to experiment with the REST API of the algorithmic platform of VIRIATO
Disclaimer: it is not meant to be published,
"""

import requests


# for some general function as a helper
def f_do_request(host_str, request_str, request_type, request_body=None, params_dict=None):
    rest_str = host_str + request_str
    if request_type == 'GET':
        rest_response = requests.get(rest_str, params=params_dict)
    elif request_type == 'POST':
        rest_response = requests.post(rest_str, json=request_body)
    elif request_type == 'PUT':
        rest_response = requests.put(rest_str, json=request_body)
    else:
        print('undefined request type, must be GET, POST, PUT')
        raise
    # if there is any error, we raise it here
    try:
        rest_response.raise_for_status()
    finally:
        print(rest_response.text)
    return rest_response


def main():
    # %% Do a GET request to test the API
    # define the host str, where ist it:
    hostStr = 'http://localhost:8080/'
    # what is the str you want to execute:
    getStr = 'parameters/train'
    # do it
    response = f_do_request(hostStr, getStr, 'GET')
    # for now, print it
    print(response.json())

    # %% Do another GET, with params this time:
    getStr = 'assignable-station-tracks-on-train-path-node?'
    paramDict = {'TrainPathNodeID': 6066}
    response = f_do_request(hostStr, getStr, 'GET', params_dict=paramDict)
    print(response.json())
    paramDict['TrainPathNodeID'] = 1167
    response = f_do_request(hostStr, getStr, 'GET', params_dict=paramDict)
    print(response.json())

    # %% Do another GET, with no params this time:
    getStr = 'section-tracks-between/1/25'
    response = f_do_request(hostStr, getStr, 'GET')
    print(response.json())

    # %% Do a POST request to test the API
    body = {
        'TrainPathNodeID': 1167,
        'NodeTrackID': '634'
    }
    postStr = 'assign-station-track'
    response = f_do_request(hostStr, postStr, 'POST', request_body=body)
    print(response.json())


if __name__ == '__main__':
    main()
