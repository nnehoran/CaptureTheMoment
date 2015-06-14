import urllib2
import json
import csv
import map_interface
import time
import math

photos_snapped = []
old_lat = 0
old_lon = 0

# query a url and return the result in JSON format
def query(url):
    json_string = urllib2.urlopen(url).read()
    return json.loads(json_string)

# read the vehicle data from the simulator (2, 3, 4, or 5)
def readVehicleData(vehicle_num):
    url = 'http://172.31.99.' + str(vehicle_num) + '/vehicle'
    return query(url)

# returns the global direction of the item at (lat,lon) from loction (my_lat,my_lon)
def getGlobalDir(my_lat, my_lon, lat, lon):
    dy = lat - my_lat
    dx = lon - my_lon
    angle = math.atan2(dy, dx)*180/math.pi - 90
    if angle <= -180:
        angle += 360
    return angle

# returns the relative direction of dir1 relative to dir2
def getRelDir(dir1, dir2):
    diff = dir1 - dir2
    if diff < -180:
        diff += 360
    elif diff >= 180:
        diff -= 360
    return diff

# snap a photo
def snapPhoto(title, direction, lat, lon, timestamp):
    photos_snapped.append(title)
    print title + ": " + str(math.floor(direction)) + " deg, " + str(timestamp)
    # do something here
    return

# , read the vehicle data, get calculate
#potential photo opportunities, and snap the photos
def main(cmmds=None):
    global old_lat
    global old_lon
    global places

    # the search radius for potential photo targets
    rad = 100

    #read the user category prefereneces
    cat = ""
    with open('place_preferences.txt', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            cat += ','.join(row)

    while(True):
        vd = readVehicleData(3)
        lat = vd.get('GPS_Latitude')
        lon = vd.get('GPS_Longitude')
        ts = vd.get('Timestamp')

        # calculate the direction of travel
        car_glob_dir = getGlobalDir(old_lat, old_lon, lat, lon)
        old_lat = lat
        old_lon = lon

        # find any good photo opportunities
        places = map_interface.getPlacesNear(lat, lon, rad, cat)

        # find the closest new photo candidate and snap the photo
        for i in places:
            title = i.get('title')
            pos = i.get('position')

            # calculate the global direction of the photo
            photo_glob_dir = getGlobalDir(lat, lon, pos[0], pos[1])

            # calculate the dirction relative to the car
            photo_rel_dir = getRelDir(photo_glob_dir, car_glob_dir)

            if not title in photos_snapped:
                snapPhoto(title, photo_rel_dir, lat, lon, ts)
                if cmmds != None:
                   cmmds.quickphoto("quickphoto", title, photo_rel_dir)
                break

        time.sleep(1)

if __name__ == "__main__":
    main()
