import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap
import json
import pickle
from JSON.service_schema_library_json import *
import ServiceConnector as services


class BlockResource(resource.Resource):
    """
    Example resource which supports GET and PUT methods. It sends large
    responses, which trigger blockwise transfer.
    """

    def __init__(self):
        super(BlockResource, self).__init__()
        self.content = ("This is the resource's default content. It is padded "\
                "with numbers to be large enough to trigger blockwise "\
                "transfer.\n" + "0123456789\n" * 100).encode("ascii")

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.content = request.payload
        payload = ("I've accepted the new payload. You may inspect it here in "\
                "Python's repr format:\n\n%r"%self.content).encode('utf8')
        return aiocoap.Message(payload=payload)



class ResourceResponder(resource.Resource):

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
       
        sdrequest = request.payload.decode('utf-8')
        payload = services.discover(sdrequest)
       
        return aiocoap.Message(payload=payload)

class LightDataResource(resource.ObservableResource):
  
    def __init__(self):
        super(LightDataResource, self).__init__()

        self.notify()

    def notify(self):
        self.updated_state()
        asyncio.get_event_loop().call_later(6, self.notify)

    def update_observation_count(self, count):
        if count:
            # not that it's actually implemented like that here -- unconditional updating works just as well
            print("Keeping the clock nearby to trigger observations")
        else:
            print("Stowing away the clock until someone asks again")

    async def render_get(self, request):
        testpayload = all_paths_finder_service_response_to_json(path_list)
        print("GLEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEBA")
        print(testpayload)
        #payload = pickle.dumps(testpayload)
        #payload = payload.encode('ascii')
        #payload = [1,2,3,4]
        payload = bytes(testpayload, 'utf-8')
	#payload = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").encode('ascii')
        return aiocoap.Message(payload=payload)



#class CoreResource(resource.Resource):
#    """
#    Example Resource that provides list of links hosted by a server.
#    Normally it should be hosted at /.well-known/core
#
#    Notice that self.visible is not set - that means that resource won't
#    be listed in the link format it hosts.
#    """
#
#    def __init__(self, root):
#        resource.Resource.__init__(self)
#        self.root = root
#
#    async def render_get(self, request):
#        data = []
#        self.root.generate_resource_list(data, "")
#        payload = ",".join(data).encode('utf-8')
#        return aiocoap.Message(payload=payload, content_format=40)

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))

#    root.add_resource(('time',), TimeResource())

    root.add_resource(('lightdata',), LightDataResource())

    root.add_resource(('other', 'block'), BlockResource())

    root.add_resource(('resourceresponder',), ResourceResponder())
#    root.add_resource(('other', 'separate'), SeparateLargeResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
