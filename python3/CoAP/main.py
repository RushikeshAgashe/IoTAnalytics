import ServiceConnector as services
import time
import math
from subprocess import call
import JSON.service_schema_library_json as tojson
import JSON.service_schema_library_raw_data as toraw


class LampSaver(object):
    def __init__(self, start = "A", end = "G", debug = False):
        self.start = start
        self.end = end
        self.debug = debug

        self.AllPathsFinderService = None
        self.HistoryService = None

    def main(self):
        self.GetMostEfficientPath(self.start, self.end)

    def GetMostEfficientPath(self, s, e):
        allPaths = self.GetAllPaths(s, e)
        allLights = self.RequestLightData(allPaths)
        allPathsLights = self.AverageAmbientLight(allPaths, allLights)
        finalPath = self.HighestAverageAmbientLight(allPathsLights)
        self.Navigate(finalPath)

    def GetAllPaths(self, s, e):
        #Trying to find the service...
        if self.debug: print("Waiting to find PathFinder service...")

        self.AllPathsFinderService = \
            self.waitForServiceConnection("allpaths", self.AllPathsFinderService)

        if self.debug: print("Waiting on results from PathFinder service...")

	request = tojson.all_paths_finder_service_request_to_json(s, e)
        response = services.send(self.AllPathsFinderService, request)
	paths = toraw.all_paths_finder_service_response_to_raw_dict(response)

        if self.debug:
            print()
            for path in paths["path_list"]:
                for point in path:
                    print(point)
                print()

        return paths

    def RequestLightData(self, paths):
        if self.debug: print("Waiting to find History service...")

        self.HistoryService = \
            self.waitForServiceConnection("history", self.HistoryService)

        if self.debug: print("Waiting on results from History service...")

        timestamp = 604
	request = tojson.light_history_service_request_to_json(paths, timestamp)
        response = services.send(self.HistoryService, request)
	lights = toraw.light_history_service_response_to_raw_dict(response)

        assert(len(lights["light_hist_list"]) == len(paths["path_list"]))
        if self.debug:
            print()
            for path in lights["light_hist_list"]:
                for point in path:
                    print(point)
                print()

        return lights

    def AverageAmbientLight(self, paths, lights):
        avgd_paths = []
        for path, light in zip(paths["path_list"], lights["light_hist_list"]):
            assert(len(path)==len(light)+1)
            totalLight, totalDist = 0, 0

            for idx, l in enumerate(light):
                a,b = path[idx:idx+2]
                totalLight += l
                totalDist = self.getDistance(a, b)

            path_value = { "path": path, "avg_light": totalLight / totalDist }
            avgd_paths.append(path_value)

        return avgd_paths

    def HighestAverageAmbientLight(self, paths_and_lights):
        if self.debug: print("Determing optimal path...")
        return max(paths_and_lights, key=lambda x : x["avg_light"])["path"]

    def Navigate(self, finalPath):
        if self.debug: print("Walking...")
        allcoords = []
        for coord in finalPath:
                allcoords.append(str(coord[0]))
                allcoords.append(str(coord[1]))
        call([".././nav"] + allcoords)

    #============

    def waitForServiceConnection(self, connectionType, prevConnection):
    	sdrequest = tojson.sd_request_to_json(connectionType)
        connection = prevConnection

        while connection is None or not services.connected(connection):
            sdresponse = client_function_put(sdrequest) 
            #sdresponse = services.discover(sdrequest)
	    connection = toraw.sd_response_to_raw_dict(sdresponse)
            if connection is None: time.sleep(1)
        return connection

    def getDistance(self, a, b):
        lat1, lng1 = a
        lat2, lng2 = b

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


if __name__ == "__main__":
    LampSaver(debug = False).main()
