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

### Here
Let's [search][here_search] for all "sights-meseums" and "leisure-outdoor"
places within an 800 meter radius of the Ferry Building:

    import here
    from util import FERRY_BUILDING_LL

    pa = dict(here.DEFAULT_PARAMS)
    pa['in'] = FERRY_BUILDING_LL + ';r=800'
    pa['cat'] = 'sights-museums,leisure-outdoor'
    result = here.search(pa)

This API returns items with an attribute, `href` that contains the place
details. Let's get the details for one:

    # using the previous result
    import util
    details = util.get(result['results']['items'][0]['href'],
                       here.DEFAULT_PARAMS)

### Yelp
Let's [search][yelp_search] for all "arts" and "realestate" near the Ferry
Building:

    import yelp
    from util import FERRY_BUILDING_LL as LL

    pa = dict(yelp.DEFAULT_PARAMS)
    la, lo = LL.split(',')
    pa['latitude'] = la
    pa['longitude'] = lo
    pa['radius'] = '800'
    pa['categories'] = 'arts,realestate'
    result = yelp.search(pa)

Let's get the [details][yelp_details] for the Exploratorium:

    import yelp
    result = yelp.details('exploratorium-san-francisco-2')

If you run into issues, note that Yelp uses OAuth under the hood so something
may have gone wrong with authentication.

[fs_search]: https://developer.foursquare.com/docs/venues/search
[fs_details]: https://developer.foursquare.com/docs/venues/venues
[gp_search]: https://developers.google.com/places/web-service/search
[gp_details]: https://developers.google.com/places/web-service/details
[here_search]: https://developer.here.com/rest-apis/documentation/places/topics_api/resource-explore.html
[yelp_search]: https://www.yelp.com/developers/documentation/v3/business_search
[yelp_details]: https://www.yelp.com/developers/documentation/v3/business
