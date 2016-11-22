from geopy.distance import vincenty
from time import sleep
from pprint import pprint as pp
import json
import yelp

SHOW_CATS = {'active',
             'arts',
             'eventservices',
             'food',
             'hotelstravel',
             'localflavor',
             'nightlife',
             'pets',
             'restaurants',
             'shopping'}

ITER = 50
DEF_PARAMS = {'latitude': 19.924043,
              'longitude': -155.887652,
              'radius': 40000,
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
            'id': place['id'],
            'coord': place['coordinates']}

def filter_places(places):
    return filter(should_show_place, places)

def should_show_place(place):
    rating = place['rating']
    review_count = place['review_count']
    cats = place['categories']
    return should_show_place_by_cats(cats) and should_show_place_by_rating(rating, review_count)

def should_show_place_by_cats(cats):
    # We whitelisted the categories so we don't need to do ^ anymore.
    return True

def should_show_place_by_rating(rating, review_count):
    if rating <= 2.5 or \
            (rating == 3 and review_count > 3):
        return False
    return True

def sort_by_distance(places):
    return sorted(places, key=lambda p: p['distance'])

def query_full(lat, lng, radius):
    params = dict(DEF_PARAMS)
    params['latitude'] = lat
    params['longitude'] = lng
    params['radius'] = radius
    places = query(params)

    # discrepency is because yelp returns fewer results than specified in total.
    print 'actual: ' + str(len(places))

    pr_places = prune_data(places)
    filtered_places = filter_places(pr_places)
    sorted_places = sort_by_distance(filtered_places)
    return sorted_places

def write_places(filename, places):
    with open(filename, 'w') as f: json.dump(places, f, indent=4)

def dedupe_places(*args):
    seen = set()
    out = []
    for place_list in args:
        for place in place_list:
            id = place['id']
            if id in seen: continue
            seen.add(id)
            out.append(place)
    return out

HOTEL_COORD = (19.924043, -155.887652)
def replace_distance_to_hotel(places):
    out = []
    for place in places:
        tmp_c = place['coord']
        coord = (tmp_c['latitude'], tmp_c['longitude'])
        dist = vincenty(HOTEL_COORD, coord).m
        place_cpy = dict(place)
        place_cpy['distance'] = dist
        out.append(place_cpy)
    return out

def rm_id(places):
    out = []
    for place in places:
        cpy = dict(place)
        if 'id' in cpy: del cpy['id']
        out.append(cpy)
    return out

# Get the items in lrg that aren't in sm.
def diff(sm, lrg):
    in_sm = set()
    for place in sm:
        in_sm.add(place['id'])

    out = []
    for place in lrg:
        if place['id'] in in_sm: continue
        cpy = dict(place)
        out.append(cpy)
    return out

# To query over 40km.
# - Make multiple individual queries (don't exceed 1000 items!)
# - call:
#   - dedupe_places(*args)
#   - replace_distance_to_hotel
#   - sort_by_distance
#   - rm_id
#   - write_places

def main():
    # note: I've never actually run this before; just in pieces in repl.
    places = query(DEF_PARAMS)
    pr_places = prune_data(places)
    filtered_places = filter_places(pr_places)
    sorted_places = sort_by_distance(filtered_places)
    pp(sorted_places)

if __name__ == '__main__':
    main()
