from time import sleep
from pprint import pprint as pp
import json
import yelp

SHOW_CATS = {'active',
             'arts',
             'beautysvc',
             'eventservices',
             'food',
             'hotelstravel',
             'localflavor',
             'massmedia',
             'nightlife',
             'pets',
             'publicservicesgovt',
             'restaurants',
             'shopping'}

HIDE_CATS = {'auto',
             "bicycles",
             "education",
             "financialservices",
             "health",
             "homeservices",
             "localservices",
             "professional",
             "realestate",
             "religiousorgs"}

ITER = 50
DEF_PARAMS = {'latitude': 19.924043,
              'longitude': -155.887652,
              'radius': 27000,
              'limit': _ITER,
              'categories': ','.join(SHOW_CATS)}
              #'sort_by': 'distance'} # breaks the total in received json

def cats_to_root_dict():
    with open('categories.json') as f:
        cats = json.load(f)

    cats_to_parents = {}
    for cat in cats:
        cats_to_parents[cat['alias']] = set(cat['parents'])

    cats_to_root = {}
    for cat in cats:
        root = get_root_category(cats_to_parents, cat['alias'])
        cats_to_root[cat['alias']] = root
    return cats_to_root

CATS_TO_ROOT = cats_to_root_dict()

def get_root_category(cats_to_parents, cat):
    parents = cats_to_parents[cat]
    if parents is None:
        print 'uh oh'
        return set()

    if len(parents) == 0:
        return set([cat])

    out = set()
    for parent in parents:
        out = out.union(get_root_category(cats_to_parents, parent))
    return out

def query(params):
    res = yelp.search(params)
    out = res['businesses']
    total = res['total']
    print 'total: ' + str(total)
    for offset in range(ITER, min(1000, total), ITER):
        #sleep(1) # avoid rate limit
        params['offset'] = offset
        res = yelp.search(params)
        out += res['businesses']
    return out

def prune_data(places):
    return map(place_to_pruned_place, places)

def place_to_pruned_place(place):
    # matching attr in https://gist.github.com/jhugman/23424345cb79b091fc335ab7e5eaf7b9
    return {'name': place['name'],
            'rating': place['rating'],
            'review_count': place['review_count'],
            'categories': map(lambda p: p['alias'], place['categories']),
            'distance': place['distance'],
            'coord': place['coordinates']}

def filter_places(places):
    return filter(should_show_place, places)

def should_show_place(place):
    rating = place['rating']
    review_count = place['review_count']
    cats = place['categories']
    return should_show_place_by_cats(cats) and should_show_place_by_rating(rating, review_count)

def should_show_place_by_cats(cats):
    cats_to_root = CATS_TO_ROOT

    roots = set()
    for cat in cats:
        roots = roots.union(cats_to_root[cat])

    if len(roots - HIDE_CATS) == 0:
        return False
    return True

def should_show_place_by_rating(rating, review_count):
    if rating <= 2.5 or \
            (rating == 3 and review_count > 3):
        return False
    return True

def sort_by_distance(places):
    return sorted(places, key=lambda p: p['distance'])

def query_full(lat, lng):
    params = dict(DEF_PARAMS)
    params['latitude'] = lat
    params['longitude'] = lng
    places = query(params)

    # discrepency is because yelp returns fewer results than specified in total.
    print 'actual: ' + str(len(places))

    pr_places = prune_data(places)
    filtered_places = filter_places(pr_places)
    sorted_places = sort_by_distance(filtered_places)
    return sorted_places

def main():
    # note: I've never actually run this before; just in pieces in repl.
    places = query(DEF_PARAMS)
    pr_places = prune_data(places)
    filtered_places = filter_places(pr_places)
    sorted_places = sort_by_distance(filtered_places)
    pp(sorted_places)

if __name__ == '__main__':
    main()
