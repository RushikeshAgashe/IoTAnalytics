import asyncio
import pdb

#import aiocoap.resource as resource
#import aiocoap
#from aiocoap import *
import CoAPlib.resource as resource
import CoAPlib as aiocoap
from CoAPlib import *

from CONSTANTS import *

from all_paths_finder_service import allpathsfinderservice
import JSONlib.service_schema_library_json as tojson
import JSONlib.service_schema_library_raw_data as toraw


class AllPathsFinderService(resource.Resource):
    """
    This service sends a list of paths from source to destination
    """
    rt = ALL_PATHS_FINDER_SERVICE
    code = "GET"

    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        payload = request.payload
        #print("{0} Received request = {1}".format(self.rt, payload))

        request = request.payload.decode('utf-8')
        request = toraw.all_paths_finder_service_request_to_raw_dict(request)
        paths = allpathsfinderservice(request['source'], request['destination'])
        resp = tojson.all_paths_finder_service_response_to_json(paths)
        resp = bytes(resp, 'utf-8')

        #print("{0} Sending response = {1}".format(self.rt, resp))
        return aiocoap.Message(payload=resp)

    def get_link_description(self):
        ret = super().get_link_description()
        if hasattr(self, 'code'):
            ret['code'] = self.code
        return ret

def main():
    root = resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource((ALL_PATHS_RESOURCE,), AllPathsFinderService())
    asyncio.Task(aiocoap.Context.create_server_context(root, bind=("", PATH_FINDER_SERVER_PORT)))
    print("Running {0} server on port {1}".format(ALL_PATHS_FINDER_SERVICE, PATH_FINDER_SERVER_PORT))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
