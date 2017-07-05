import datetime
import logging
import asyncio
import CoAPlib.resource as resource
import CoAPlib as aiocoap
from CONSTANTS import *
from all_paths_finder_service import allpathsfinderservice
from light_history_service import get_link_averages as lighthistoryservice
import JSONlib.service_schema_library_json as tojson
import JSONlib.service_schema_library_raw_data as toraw

class AllPathsFinderService(resource.Resource):
    """
    This service sends a list of paths from source to destination
    """
    rt = ALL_PATHS_FINDER_SERVICE
    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        request = request.payload.decode('utf-8')
        request = toraw.all_paths_finder_service_request_to_raw_dict(request)
        paths = allpathsfinderservice(request['source'], request['destination'])
        resp = tojson.all_paths_finder_service_response_to_json(paths)
        resp = bytes(resp, 'utf-8')
        return aiocoap.Message(payload=resp)

class LightHistoryService(resource.Resource):
    """
    """
    rt = LIGHT_HISTORY_SERVICE
    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        request = request.payload.decode('utf-8')
        request = toraw.light_history_service_request_to_raw_dict(request)
        lights = lighthistoryservice(request['path_list']['path_list'], request['time_stamp'])
        resp = tojson.light_history_service_response_to_json(lights)
        print (lights)
        resp = bytes(resp, 'utf-8')
        return aiocoap.Message(payload=resp)

def main():
    root = resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource((ALL_PATHS_RESOURCE,), AllPathsFinderService())
    root.add_resource((LIGHT_HISTORY_RESOURCE,), LightHistoryService())
    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    print("Runing Coap Server")
    main()
