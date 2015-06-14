import urllib2
import json
import csv

app_id = 'eRi9NLd3fZJeHOH2we6g'
app_code = 'I2perok5rTYVAbGvJ3DFgg'
base_url = 'http://places.cit.api.here.com/places/v1/discover/around'
latitude = 40.74917
longitude = -73.98529



def query(url):
    json_string = urllib2.urlopen(url).read()
    return json.loads(json_string)

def queryLocation(lat, lon, rad, cat):
    at_str =  str(lat) + ',' + str(lon)
    in_str = at_str + ';r=' + str(rad)
    url = base_url + '?in=' + in_str + '&cat=' + cat + '&app_id=' + app_id + '&app_code=' + app_code + '&tf=plain&pretty=true'
    return query(url)
    
def getItems(json_object):
    j = json_object
    items = None
    if 'results' in j:
        results = j.get('results')
        if 'items' in results:
            items = results.get('items')
    elif 'items' in j:
        items = j.get('items')
    result_list = []
    for i in items:
        title = i.get('title')
        item_id = i.get('category').get('id')
        dist = i.get('distance')
        rating = i.get('averageRating')
        result_list.append([title, item_id, dist])
    return result_list
    
def getNext(json_object):
    j = json_object
    next = None
    if 'results' in j:
        results = j.get('results')
        if 'next' in results:
            next = results.get('next')
    elif 'next' in j:
        next = j.get('next')
    return next

def getPlacesNear(lat, lon, rad, cat):
    query_result = queryLocation(lat, lon, rad, cat)
    result = getItems(query_result)
    next = getNext(query_result)
    while next != None:
        query_result = query(next)
        result += getItems(query_result)
        print "hit"
        next = getNext(query_result)
    return result

def main():

    max_rad = 150
    cat = ""

    with open('place_preferences.txt', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            cat += ','.join(row)

    places = getPlacesNear(37.413088, -121.965200, max_rad, cat)
    for i in range(len(places)):
        print places[i]

if __name__ == "__main__":
    main()
