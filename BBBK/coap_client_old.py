import pdb
import logging
import asyncio

import JSONlib.service_schema_library_json as tojson
import JSONlib.service_schema_library_raw_data as toraw
from CoAPlib import *
import link_header as lh


__all__ = ["coap_discover_resources", "coap_client_get"]


async def _discover_resources(call_obj, ip):
    """
    Discovers resources hosted on a CoAP server with IP address as ip
    Does this by sending a GET request on coap://ip /.well_known/core
    :param ip: <string> IpV4 Address
    :return: <dictionary>  {rt -> uri}
    """
    context = 'coap://' + ip
    protocol = await Context.create_client_context()
    uri = context + "/.well-known/core"
    #print (uri)

    request = Message(code=GET, uri=uri)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print("Failed to discover resources on {0}".format(uri))
        print(e)
        exit(-1)
    #pdb.set_trace()
    payload = str(response.payload)[2:-1]
    links = lh.parse(payload).links
    # Sorry, couldn't find a better way
    links = [(link.rt[0], link.get_target(context)) for link in links if 'rt' in link]
    res = {link[0]: link[1] for link in links}
    #print(res)
    #pdb.set_trace()
    if call_obj:
        call_obj.resourceDict = res
    return res


async def _client_get(uri, payload, call_obj):
    protocol = await Context.create_client_context()
    #payload = {"source":"A", "destination":"G"}
    #src = "A"
    #dest = "G"
    #payload = tojson.all_paths_finder_service_request_to_json(src,dest) 
    payload = bytes(payload, 'utf-8')
    request = Message(code=GET, uri=uri, payload=payload)
    
    try:
        response = await protocol.request(request).response
        print("RESPONSE")
        #print (response)
        #pdb.set_trace()
    except Exception as e:
        print("Failed while getting resource for uri= {0}, payload={1}".format(uri, payload))
        print(e)
        exit(-1)
    payload = response.payload
    call_obj.response = payload.decode('utf-8')
    #print (response)

def coap_discover_resources(call_obj=None, ip="localhost"):
    asyncio.get_event_loop().run_until_complete(_discover_resources(call_obj, ip))

def coap_client_get(uri, payload, response):
    asyncio.get_event_loop().run_until_complete(_client_get(uri, payload, response))


def _client_put(uri, payload):
    pass


if __name__ == "__main__":
    coap_discover_resources()
