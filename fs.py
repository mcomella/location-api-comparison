import util
from functools import partial

URL_SEARCH = 'https://api.foursquare.com/v2/venues/search'
URL_EXPLORE = 'https://api.foursquare.com/v2/venues/explore'
URL_VENUE = 'https://api.foursquare.com/v2/venues/'

_VERSION = '20160928'
_MODE = 'foursquare'

_keys = util.get_keys('foursquare')
assert 'client_id' in _keys
assert 'client_secret' in _keys

DEFAULT_PARAMS = dict({'v': _VERSION,
                       'm': _MODE}.items() + _keys.items())

def _get(url, params):
    return util.get(url, params)['response']

search = partial(_get, URL_SEARCH)
explore = partial(_get, URL_EXPLORE)

def details(venue_id):
    return _get(URL_VENUE + venue_id, DEFAULT_PARAMS)
