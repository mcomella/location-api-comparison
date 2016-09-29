from functools import partial
import util

# There is a python client library [1] but the places search is broken in that
# it requires you to make a query, which is not required by the REST API.
#
# [1]: https://github.com/googlemaps/google-maps-services-python

URL_SEARCH = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
URL_DETAILS = 'https://maps.googleapis.com/maps/api/place/details/json'

_keys = util.get_keys('gplaces')
assert 'key' in _keys

DEFAULT_PARAMS = _keys

def _get(url, is_result_plural, params):
    key = 'results' if is_result_plural else 'result'
    return util.get(url, params)[key]

search = partial(_get, URL_SEARCH, True)
details = partial(_get, URL_DETAILS, False)
