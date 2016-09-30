import util

_PATH = 'https://places.cit.api.here.com/places/v1/'
_URL_EXPLORE = _PATH + 'discover/explore'

DEFAULT_PARAMS = util.get_keys('here')
assert 'app_id' in DEFAULT_PARAMS
assert 'app_code' in DEFAULT_PARAMS

def search(params):
    return util.get(_URL_EXPLORE, params)
