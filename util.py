import json
import requests

_KEY_FILE = 'keys.json'

FERRY_BUILDING_LL = '37.795,-122.396'

def get(url, params):
    return requests.get(url, params).json()

def post(url, params):
    return requests.post(url, params).json()

def get_keys(key_type):
    with open(_KEY_FILE) as f:
        return json.load(f)[key_type]
