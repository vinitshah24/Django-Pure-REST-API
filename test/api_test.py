import json
import requests

BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "api/blog/"


def get_list(id=None):
    data = json.dumps({})
    if id is not None:
        data = json.dumps({"id": id})
    r = requests.get(f'{BASE_URL}/{ENDPOINT}', data=data)
    return r.json() if r.status_code == 201 else f'ERROR CODE: {r.status_code}'


def create_blog():
    new_data = {
        'user': 1,
        "content": "We The Best!"
    }
    r = requests.post(f'{BASE_URL}/{ENDPOINT}', data=json.dumps(new_data))
    # print(r.headers)
    return r.json() if r.status_code == 201 else f'ERROR CODE: {r.status_code}'


def update_blog():
    new_data = {
        "id": 9,
        "content": "Pure Django!"
    }
    r = requests.put(f'{BASE_URL}/{ENDPOINT}', data=json.dumps(new_data))
    print(r.status_code)
    return r.json() if r.status_code == 201 else f'ERROR CODE: {r.status_code}'


def delete_blog():
    new_data = {"id": 9}
    r = requests.delete(f'{BASE_URL}/{ENDPOINT}', data=json.dumps(new_data))
    print(r.status_code)
    return r.json() if r.status_code == 201 else f'ERROR CODE: {r.status_code} => {r.text}'


# http://127.0.0.1:8000/api/blog/
# print(get_list())
# print(get_list(1))
# print(create_blog())
# print(update_blog())
# print(delete_blog())


# url = "http://127.0.0.1:8000/api/blog/1"
# response = requests.request("GET", url)
# print(response.json())

# payload = {}
# response = requests.request("POST", url, data=payload)
# print(response.text)

# payload = {
#     'user': 1,
#     "content": "Another 1!"}
# response = requests.request("PUT", url, data=payload)
# print(response.text)

# response = requests.request("DELETE", url)
# print(response.text)
