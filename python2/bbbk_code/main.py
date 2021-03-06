import sys
import os

sys.path.append(sys.path[0] + "\\..");
os.chdir(sys.path[-1])

import bbbk_code.ServiceConnector as services
import time
import math

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

        paths = services.send(self.AllPathsFinderService, \
                             { "start": s, "end": e })

        if self.debug:
            print()
            for path in paths:
                for point in path:
                    print(point)
                print()

        return paths

    def RequestLightData(self, paths):
        if self.debug: print("Waiting to find History service...")

        self.HistoryService = \
            self.waitForServiceConnection("history", self.HistoryService)

        if self.debug: print("Waiting on results from History service...")
        lights = services.send(self.HistoryService, \
                             { "paths": paths })

        assert(len(lights) == len(paths))
        if self.debug:
            print()
            for path in lights:
                for point in path:
                    print(point)
                print()

        return lights

    def AverageAmbientLight(self, paths, lights):
        avgd_paths = []
        for path, light in zip(paths, lights):
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
        for p in finalPath: print(p)

    #============

    def waitForServiceConnection(self, connectionType, prevConnection):
        connection = prevConnection
        while connection is None or not services.connected(connection):
            connection = services.service_discovery_request(connectionType)
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
    LampSaver(debug = True).main()
