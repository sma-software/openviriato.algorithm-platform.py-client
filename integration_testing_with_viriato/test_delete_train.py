import requests



if __name__ == '__main__':
    response_obj = requests.request("DELETE","http://localhost:8080/trains/1193")
    print(response_obj.json())