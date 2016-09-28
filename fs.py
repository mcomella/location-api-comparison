import json
from util import KEY_FILE

URL_SEARCH = 'https://api.foursquare.com/v2/venues/search'
URL_EXPLORE = 'https://api.foursquare.com/v2/venues/explore'

_VERSION = '20160928'
_MODE = 'foursquare'

with open(KEY_FILE) as f:
    _keys = json.load(f)['foursquare']
assert 'client_id' in _keys
assert 'client_secret' in _keys

DEFAULT_PARAMS = dict({'v': _VERSION,
                       'm': _MODE}.items() + _keys.items())
