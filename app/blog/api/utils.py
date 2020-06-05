import json


def is_vaid_json(json_data):
    try:
        data = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid
