import asyncio
import time
import threading
import math
import pdb
import pprint

from subprocess import call
from CoAPlib import resource
import CoAPlib as aiocoap
from coap_client import *
from CONSTANTS import *

import JSONlib.service_schema_library_json as tojson
import JSONlib.service_schema_library_raw_data as toraw

test_timestamp = 1236

class LampSaver(object):
    def __init__(self, start = "E", end = "N", debug = False):
        self.start = start
        self.end = end
        self.debug = debug
        self.resourceDict = None
        self.AllPathsFinderService = None
        self.LightHistoryService = None
        self.response = None

        #p = threading.Thread(target=self.light_server)
        #p.setDaemon(True)
        #p.start()

    def main(self):
        coap_discover_resources(self)
        self.GetMostEfficientPath(self.start, self.end)

    def GetMostEfficientPath(self, s, e):
        pp = pprint.PrettyPrinter(indent=4)
        allPaths = self.GetAllPaths(s, e)
        allLights = self.RequestLightData(allPaths)
        allPathsLights = self.AverageAmbientLight(allPaths, allLights)
        
        average_light_list = []
        for x in range(0,len(allPathsLights)):
            average_light_list.append(allPathsLights[x]['avg_light'])
        
       	if self.debug: pp.pprint(average_light_list)
        finalPath = self.HighestAverageAmbientLight(allPathsLights)

        if self.debug: print("FINAL PATH"); pp.pprint(finalPath);
        self.Navigate(finalPath)

    def GetAllPaths(self, s, e):
        #TODO: Service discovery
        self.AllPathsFinderService = self.resourceDict[ALL_PATHS_FINDER_SERVICE]

        if self.debug: print("\nWaiting on results from AllPathsFinderService...")

        request = tojson.all_paths_finder_service_request_to_json(s, e)
        coap_client_get(self.AllPathsFinderService, request, self)
        paths = toraw.all_paths_finder_service_response_to_raw_dict(self.response)

        if self.debug: pprint.PrettyPrinter(indent=4).pprint(paths)
        return paths

    def RequestLightData(self, paths):
        #TODO: Service discovery
        self.LightHistoryService = self.resourceDict[LIGHT_HISTORY_SERVICE]
        if self.debug: print("\nWaiting on results from LightHistoryService...")

        timestamp = str(test_timestamp).zfill(4) #TODO: Get timestamp from GPS.
        request = tojson.light_history_service_request_to_json(paths, timestamp)
        coap_client_get(self.LightHistoryService, request, self)
        lights = toraw.light_history_service_response_to_raw_dict(self.response)

        if self.debug: pprint.PrettyPrinter(indent=4).pprint(lights)
        assert(len(lights["light_hist_list"]) == len(paths["path_list"]))

        return lights

    def AverageAmbientLight(self, paths, lights):
        avgd_paths = []
        for path, light in zip(paths["path_list"], lights["light_hist_list"]):
            assert (len(path) == len(light) + 1)
            totalLight, totalDist = 0, 0

            for idx, l in enumerate(light):
                a, b = path[idx:idx + 2]
                totalLight += l
                totalDist = self.getDistance(a, b)

            path_value = { "path": path, "avg_light": totalLight / len(path) }
            avgd_paths.append(path_value)

        return avgd_paths

    def HighestAverageAmbientLight(self, paths_and_lights):
        if self.debug: print("\nDeterming optimal path...")

        return max(paths_and_lights, key=lambda x : x["avg_light"])["path"]

    def Navigate(self, finalPath):
        if self.debug: print("\nWalking...")
        allcoords = []

        pprint.PrettyPrinter(indent=4).pprint(finalPath)
        for coord in finalPath:
            allcoords.append(str(coord[0]))
            allcoords.append(str(coord[1]))
        call(["./nav"] + allcoords)

    # ============

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
        R = 6371000  # radius of earth in m
        lat1rads = math.radians(lat1)
        lat2rads = math.radians(lat2)
        deltaLat = math.radians((lat2 - lat1))
        deltaLng = math.radians((lng2 - lng1))
        a = math.sin(deltaLat / 2) * math.sin(deltaLat / 2) + math.cos(lat1rads) * math.cos(lat2rads) * math.sin(
            deltaLng / 2) * math.sin(deltaLng / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return d

    #=============

    def light_server(self):
        root = resource.Site()
        root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
        root.add_resource(('light',), LightResource())

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.Task(aiocoap.Context.create_server_context(root, loop=loop))
        loop.run_forever()

class LightResource(resource.Resource):
    def __init__(self):
        super(LightResource, self).__init__()

    async def render_get(self, request):
        payload = "Three rings for the elven kings under the sky, seven rings " \
                  "for dwarven lords in their halls of stone, nine rings for " \
                  "mortal men doomed to die, one ring for the dark lord on his " \
                  "dark throne.".encode('ascii')
        return aiocoap.Message(payload=payload)


if __name__ == "__main__":
    LampSaver(debug = False).main()
