import math
import csv
import ast

def getPathLength(lat1,lng1,lat2,lng2):
    '''calculates the distance between two lat, long coordinate pairs'''
    R = 6371000 # radius of earth in m
    lat1rads = math.radians(lat1)
    lat2rads = math.radians(lat2)
    deltaLat = math.radians((lat2-lat1))
    deltaLng = math.radians((lng2-lng1))
    a = math.sin(deltaLat/2) * math.sin(deltaLat/2) + math.cos(lat1rads) * math.cos(lat2rads) * math.sin(deltaLng/2) * math.sin(deltaLng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def getDestinationLatLong(lat,lng,azimuth,distance):
    '''returns the lat an long of destination point 
    given the start lat, long, aziuth, and distance'''
    R = 6378.1 #Radius of the Earth in km
    brng = math.radians(azimuth) #Bearing is degrees converted to radians.
    d = distance/1000 #Distance m converted to km
    lat1 = math.radians(lat) #Current dd lat point converted to radians
    lon1 = math.radians(lng) #Current dd long point converted to radians
    lat2 = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1)* math.sin(d/R)* math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d/R)* math.cos(lat1), math.cos(d/R)- math.sin(lat1)* math.sin(lat2))
    #convert back to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return[lat2, lon2]

def calculateBearing(lat1,lng1,lat2,lng2):
    '''calculates the azimuth in degrees from start point to end point'''
    startLat = math.radians(lat1)
    startLong = math.radians(lng1)
    endLat = math.radians(lat2)
    endLong = math.radians(lng2)
    dLong = endLong - startLong
    dPhi = math.log(math.tan(endLat/2.0+math.pi/4.0)/math.tan(startLat/2.0+math.pi/4.0))
    if abs(dLong) > math.pi:
         if dLong > 0.0:
             dLong = -(2.0 * math.pi - dLong)
         else:
             dLong = (2.0 * math.pi + dLong)
    bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0;
    return bearing

def main(interval,azimuth,lat1,lng1,lat2,lng2):
    '''returns every coordinate pair inbetween two coordinate 
    pairs given the desired interval'''

    d = getPathLength(lat1,lng1,lat2,lng2)
    remainder, dist = math.modf((d / interval))
    counter = float(interval)
    coords = []
    coords.append([lat1,lng1])
    for distance in xrange(0,int(dist)):
        coord = getDestinationLatLong(lat1,lng1,azimuth,counter)
        counter = counter + float(interval)
        coords.append(coord)
    coords.append([lat2,lng2])
    return coords

#point interval in meters
interval = 5.0
#direction of line in degrees
#start point

##with open('all_paths.csv') as f:
##    all_paths=[list(line) for line in csv.reader(f)]
##
###print all_paths
##all_coordinates = []
##with open('path_vertices_coordinates.csv') as f:
##    coordinatesWithVertex = [list(line) for line in csv.reader(f)]
##
##coordinateDict = {d[0]: d[1:] for d in coordinatesWithVertex}
##
##for i in range(0,len(coordinatesWithVertex)):
##    all_coordinates.append(coordinatesWithVertex[i][1:]) 
##
##for i in range(0,len(all_coordinates)):
##    x,y = all_coordinates[i]
##    all_coordinates[i] = [float(x),float(y)]
##
##for d in coordinateDict:
##    coordinateDict[d] = all_coordinates[i]
##
##path_coordinates = []
##temp = []
##for i in range (len(all_paths)):
##    for j in range (len(all_paths[i])):
##        temp.append(coordinateDict[all_paths[i][j]])
##    path_coordinates.append(temp)
##
###print path_coordinates
##
##with open('all_paths_coordinates.csv','wb') as out:
##    csv_out=csv.writer(out)
##    for row in path_coordinates:
##        csv_out.writerow(row)
##

with open('all_paths_coordinates.csv') as f:
   all_paths_coordinates=[line for line in csv.reader(f)]

new_list = []
for i in range(0, len(all_paths_coordinates)):
    for j in range(0, len(all_paths_coordinates[i])):
        new_list.append(eval(all_paths_coordinates[i][j]))
    all_paths_coordinates[i] = new_list;
    new_list = []
    
all_waypoints = []
for i in range(0, len(all_paths_coordinates)):
    all_coordinates = all_paths_coordinates[i]
    counter = 0
    coordlist = [all_coordinates[0]]
    for x in range(0,len(all_coordinates)-1):  
        pt1=x
        pt2=x+1
        lat1 = all_coordinates[pt1][0]
        lng1 = all_coordinates[pt1][1]
        #end point
        lat2 = all_coordinates[pt2][0]
        lng2 = all_coordinates[pt2][1]
        azimuth = calculateBearing(lat1,lng1,lat2,lng2)
        #print azimuth
        coords = main(interval,azimuth,lat1,lng1,lat2,lng2)
        coordlist = coordlist + coords[1:]
        counter = counter+1
    all_waypoints.append(coordlist)

with open('waypoints.csv','wb') as out:
    csv_out=csv.writer(out)
    for row in all_waypoints[0]:
        csv_out.writerow(row)
    #csv_out.writerow('\n')
##    
##for i in range(0, len(all_waypoints)):
##    with open('waypoints.csv','a') as out:
##        csv_out=csv.writer(out)
##        for row in all_waypoints[i]:
##            csv_out.writerow(row)
##        #csv_out.writerow('\n')
