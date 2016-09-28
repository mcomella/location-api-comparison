import requests

KEY_FILE = 'keys.json'

FERRY_BUILDING_LL = '37.795,-122.396'

def get(url, params):
    return requests.get(url, params).json()['response']
