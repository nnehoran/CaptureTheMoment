import urllib2
import json
import csv

app_id = 'As1AGESV4Qio_HDgNw9U'
app_code = 'N4_fgYJCwnzTPt2MGmRS8A'
base_url = 'http://places.cit.api.here.com/places/v1/discover/around'
latitude = 40.74917
longitude = -73.98529


# query a url and return the result in JSON format
def query(url):
    json_string = urllib2.urlopen(url).read()
    return json.loads(json_string)

# query HERE maps for places given GPS coordinates, a radius, and a comma-separated list of categories
def queryLocation(lat, lon, rad, cat):
    at_str =  str(lat) + ',' + str(lon)
    in_str = at_str + ';r=' + str(rad)
    url = base_url + '?in=' + in_str + '&cat=' + cat + '&app_id=' + app_id + '&app_code=' + app_code + '&tf=plain&pretty=true'
    return query(url)
    
# parse the given JSON and extract the place items from it
def getItems(json_object):
    j = json_object
    items = None
    if 'results' in j:
        results = j.get('results')
        if 'items' in results:
            items = results.get('items')
    elif 'items' in j:
        items = j.get('items')
    return items
    
# check if there is a next page, and if so, return its URL
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

# query HERE maps for place date near a location, and parse through all of the
# pages of data, compiling it together
def getPlacesNear(lat, lon, rad, cat):
    query_result = queryLocation(lat, lon, rad, cat)
#    print query_result
 #   print "\n\n\n\n\n"
    result = getItems(query_result)
#    print result
#    next = getNext(query_result)
#    while next != None:
#        query_result = query(next)
#        result += getItems(query_result)
#        print "hit"
#        next = getNext(query_result)
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
