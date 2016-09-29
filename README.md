# location API comparison
Compare location APIs in a Python REPL.

## Setup

    # TODO: create a keys.json file before REPL.
    # Assuming you have virtualenv installed...
    virtualenv venv                  # create virtualenv
    source venv/bin/activate         # use virtualenv
    pip install -r requirements.txt  # install deps
    python                           # start REPL

TODO: explain keys.json.

## Sample queries
These sample queries assume you have nothing imported yet.

When you get the JSON results, it's recommended to try pretty printing them at
various depth levels:

    from pprint import pprint as pp
    pp(result, depth=3)


### Foursquare
Let's [search][fs_search] for all Museums and Public Art pieces (category
types) within an 800 meter radius of the Ferry Building:

    import fs
    from util import FERRY_BUILDING_LL

    pa = dict(fs.DEFAULT_PARAMS)
    pa['categoryId'] = '4bf58dd8d48988d181941735,507c8c4091d498d9fc8c67a9'
    pa['radius'] = 800
    pa['ll'] = FERRY_BUILDING_LL
    result = fs.search(pa)

Let's get the [details][fs_details] on the Ferry Building:

    import fs
    result = fs.details('43067280f964a52023271fe3')

### Google Places
Let's [search][gp_search] for all "point of interest"s (a place type) within an
800 meter radius of the Ferry Building:

    import gp
    from util import FERRY_BUILDING_LL

    pa = dict(gp.DEFAULT_PARAMS)
    pa['keyword'] = 'point of interest'
    pa['radius'] = 800
    pa['location'] = FERRY_BUILDING_LL
    result = gp.search(pa)

Let's get the [details][gp_details] on the Transamerica Pyramid:

    import gp

    pa = dict(gp.DEFAULT_PARAMS)
    pa['placeid'] = 'ChIJQ-U7wYqAhYAReKjwcBt6SGU'
    result = gp.details(pa)

[fs_search]: https://developer.foursquare.com/docs/venues/search
[fs_details]: https://developer.foursquare.com/docs/venues/venues
[gp_search]: https://developers.google.com/places/web-service/search
[gp_details]: https://developers.google.com/places/web-service/details
