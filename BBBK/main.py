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
from CoAPlib import *
from CONSTANTS import *

import JSONlib.service_schema_library_json as tojson
import JSONlib.service_schema_library_raw_data as toraw

from sd_client import discover_all_paths_finder_service, discover_history_service

test_timestamp = 936
class LampSaver(object):
    def __init__(self, start = [35.773637, -78.674057], \
                       end = [35.768571, -78.678672], \
                       debug = True):
        self.start = start
        self.end = end
        self.debug = debug
        self.response = None #Will be set by various server responses.

    '''
    The driving function that is called when a thread is created for this.
    '''
    def main(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.GetMostEfficientPath(self.start, self.end)

    '''
    Contains all the major steps for navigation:
        Communicate with service to get all possible paths from start to end.
        Communicate with service to get light values along each path.
        Ping all live user nodes to see if we can get more recent light values.
        Choose the path with the highest average light.
        Navigate on that path.
    '''
    def GetMostEfficientPath(self, s, e):
        pp = pprint.PrettyPrinter(indent=4)
        allPaths = self.GetAllPaths(s, e)
        allLights = self.RequestLightData(allPaths)
        allPathsLights = self.AverageAmbientLight(allPaths, allLights)
        #TODO: Get live data from user nodes.
        
       	if self.debug: 
            average_light_list = []
            for x in range(0,len(allPathsLights)):
                average_light_list.append(allPathsLights[x]['avg_light'])
            pp.pprint(average_light_list)

        finalPath = self.HighestAverageAmbientLight(allPathsLights)

        if self.debug: print("FINAL PATH"); pp.pprint(finalPath);
        self.Navigate(finalPath)

    '''
    Communicate with service to get all possible paths from start to end.
    Wait until the service can be found, then discover the appropriate resource.
    Then send and receive.
    '''
    def GetAllPaths(self, s, e):
        self.findResource(ALL_PATHS_FINDER_SERVICE,    
            discover_all_paths_finder_service)       

        if self.debug: print("\nWaiting on results from AllPathsFinderService...")

        request = tojson.all_paths_finder_service_request_to_json(s, e)
        coap_client_get(self, self.response[ALL_PATHS_FINDER_SERVICE].uri, request)
        paths = toraw.all_paths_finder_service_response_to_raw_dict(self.response)

        if self.debug: pprint.PrettyPrinter(indent=4).pprint(paths)
        return paths

    '''
    Communicate with service to get all average lights on all paths.
    Wait until the service can be found, then discover the appropriate resource.
    Then send and receive.
    '''
    def RequestLightData(self, paths):
        self.findResource(LIGHT_HISTORY_SERVICE,    
            discover_history_service)    

        if self.debug: print("\nWaiting on results from LightHistoryService...")

        timestamp = str(test_timestamp).zfill(4) #TODO: Get timestamp from GPS.
        request = tojson.light_history_service_request_to_json(paths, timestamp)
        coap_client_get(self, self.response[LIGHT_HISTORY_SERVICE].uri, request)
        lights = toraw.light_history_service_response_to_raw_dict(self.response)

        if self.debug: pprint.PrettyPrinter(indent=4).pprint(lights)
        assert(len(lights["light_hist_list"]) == len(paths["path_list"]))

        return lights

    '''
    Get the average light level for each path, considering both the historical
    data and the live data.
    '''
    def AverageAmbientLight(self, paths, lights):
        avgd_paths = []
        SCALE_FACTOR = 10
        for path, light in zip(paths["path_list"], lights["light_hist_list"]):
            assert (len(path) == len(light) + 1)
            lightScaledDistance, totalDist = 0, 0

            for idx, l in enumerate(light):
                a, b = path[idx:idx + 2]
                dist = self.getDistance(a, b)
                lightScaledDistance += (dist/(l+0.1))*SCALE_FACTOR
                totalDist += dist
            
            path_value = { "path": path, "avg_light": lightScaledDistance }
            avgd_paths.append(path_value)

        return avgd_paths

    '''
    Iterate through all average lights and pick the path with the highest.
    '''
    def HighestAverageAmbientLight(self, paths_and_lights):
        if self.debug: print("\nDeterming optimal path...")
         
        return min(paths_and_lights, key=lambda x : x["avg_light"])["path"]

    '''
    Pass the path coordinates into navigation program.
    '''
    def Navigate(self, finalPath):
        if self.debug: print("\nWalking...")
        allcoords = []

        pprint.PrettyPrinter(indent=4).pprint(finalPath)
        with open("./finalpath.csv", "w") as f:
            strs = ["%s, %s"%(str(x[0]),str(x[1])) for x in finalPath]
            full = "\n".join(strs)
            f.write(full)

        for coord in finalPath:
            allcoords.append(str(coord[0]))
            allcoords.append(str(coord[1]))
        call(["./nav"] + allcoords)

    # ============

    '''
    Find a desired service, given the type and the provided service discovery function
    in the sd_client file.
    '''
    def findResource(self, service_type, discover_service_func):
        resps = discover_service_func()
        while resps is None:
            time.sleep(1); print("sleeping...")
            resps = discover_service_func()

        for resp in resps:
            data, addr = resp
            coap_discover_resources(self,
                data[SERVICE_IP_ADDR], data[SERVICE_PORT])
            if self.response is not None: return

        raise NotImplementedError()

    '''
    Given two points, calculate the distance in meters between them.
    '''
    def getDistance(self, a, b):
        lat1, lng1 = a
        lat2, lng2 = b

        '''calculates the distance between two lat, long coordinate pairs'''
        R = 6371000  # radius of earth in m
        lat1rads = math.radians(lat1)
        lat2rads = math.radians(lat2)
        deltaLat = math.radians((lat2 - lat1))
        deltaLng = math.radians((lng2 - lng1))
        a = math.sin(deltaLat / 2) * math.sin(deltaLat / 2) + \
            math.cos(lat1rads) * math.cos(lat2rads) * math.sin(
            deltaLng / 2) * math.sin(deltaLng / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return d

    #=============

    '''def light_server(self):
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
        return aiocoap.Message(payload=payload)'''

if __name__ == "__main__":
    while(1):
        try:
            LampSaver(debug = True).main()
        except Exception :
            pass
