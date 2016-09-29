import util

URL_SEARCH = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

_keys = util.get_keys('gplaces')
assert 'key' in _keys

DEFAULT_PARAMS = _keys

def get(url, params):
    return util.get(url, params)['results']
