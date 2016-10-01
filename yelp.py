import requests
import util

_URL_AUTHENTICATE = 'https://api.yelp.com/oauth2/token'
_URL_SEARCH = 'https://api.yelp.com/v3/businesses/search'

_is_authenticated = False
_access_token = ''

_keys = util.get_keys('yelp')
assert 'client_id' in _keys
assert 'client_secret' in _keys
_authentication_keys = dict(_keys.items() + \
                            {'grant_type': 'client_credentials'}.items())

def _authenticate():
    global _is_authenticated
    global _access_token
    _access_token = util.post(_URL_AUTHENTICATE, _authentication_keys)['access_token']
    assert _access_token
    _is_authenticated = True

def search(params):
    if not _is_authenticated: _authenticate()
    return requests.get(_URL_SEARCH, params=params,
                        headers={'Authorization': 'Bearer ' + _access_token}).json()
