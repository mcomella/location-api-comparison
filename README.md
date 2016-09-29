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

## Sample query
Using the Foursquare API, let's find all Museums and Public Art pieces within
an 800 meter radius of the Ferry Building:

    import fs
    from util import FERRY_BUILDING_LL

    pa = dict(fs.DEFAULT_PARAMS)
    pa['categoryId'] = '4bf58dd8d48988d181941735,507c8c4091d498d9fc8c67a9'
    pa['radius'] = 800
    pa['ll'] = FERRY_BUILDING_LL
    res = fs.get(fs.URL_SEARCH, pa)

The JSON results are stored in `res`. You may wish to pretty print it:

    from pprint import pprint as pp
    pp(res, depth=3)
