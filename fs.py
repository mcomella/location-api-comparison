import util

URL_SEARCH = 'https://api.foursquare.com/v2/venues/search'
URL_EXPLORE = 'https://api.foursquare.com/v2/venues/explore'

_VERSION = '20160928'
_MODE = 'foursquare'

_keys = util.get_keys('foursquare')
assert 'client_id' in _keys
assert 'client_secret' in _keys

DEFAULT_PARAMS = dict({'v': _VERSION,
                       'm': _MODE}.items() + _keys.items())

def get(url, params):
    return util.get(url, params)['response']
