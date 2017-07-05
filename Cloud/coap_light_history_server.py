import asyncio
import pdb

#import aiocoap.resource as resource
#import aiocoap
import CoAPlib.resource as resource
import CoAPlib as aiocoap
from CoAPlib import *
#from aiocoap import *

from CONSTANTS import *

from light_history_service import get_link_averages as lighthistoryservice
import JSONlib.service_schema_library_json as tojson
import JSONlib.service_schema_library_raw_data as toraw

class LightHistoryService(resource.Resource):
    rt = LIGHT_HISTORY_SERVICE
    code = "GET"

    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        payload = request.payload
        #print("{0} Received request = {1}".format(self.rt, payload))

        request = request.payload.decode('utf-8')
        request = toraw.light_history_service_request_to_raw_dict(request)
        lights = lighthistoryservice(request['path_list']['path_list'], request['time_stamp'])
        resp = tojson.light_history_service_response_to_json(lights)
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
    root.add_resource((LIGHT_HISTORY_RESOURCE,), LightHistoryService())
    asyncio.Task(aiocoap.Context.create_server_context(root, bind=("", LIGHT_HISTORY_SERVER_PORT)))
    print("Running {0} server on port {1}".format(LIGHT_HISTORY_SERVICE, LIGHT_HISTORY_SERVER_PORT))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()

