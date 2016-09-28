# location API comparison
Compare location APIs in a Python REPL.

## Setup

    # TODO: create a keys.json file before REPL.
    pip install -r requirements.txt  # install deps
    source venv/bin/activate         # use deps
    python                           # start REPL

TODO: explain keys.json.

## Sample query
Using the Foursquare API:

    import fs
    from util import get, FERRY_BUILDING_LL as ll

    pa = dict(fs.DEFAULT_PARAMS)
    pa['categoryId'] = '4bf58dd8d48988d181941735,507c8c4091d498d9fc8c67a9'
    pa['radius'] = 800
    pa['ll'] = ll
    r = get(fs.URL_SEARCH, pa)

The JSON results are stored in 'r'. You may wish to pretty print it:

    from pprint import pprint as pp
    pp(r, depth=3)
