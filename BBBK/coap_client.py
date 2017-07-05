import asyncio
import pdb
from collections import namedtuple
import CoAPlib.resource as resource
import CoAPlib as aiocoap
from CoAPlib import *

import link_header as lh

from CONSTANTS import *
uri_ = namedtuple("uri_", "uri, code")

async def _coap_discover_resources(calling_obj, ip, port):
    """
    Discovers resources hosted on a CoAP server with IP address as ip and port as port
    Does this by sending a GET request on coap://ip /.well_known/core
    :param ip: <string> IpV4 Address
    :return: <dictionary>  {rt -> uri}
    """
    context = 'coap://' + ip + ':' + str(port)
    protocol = await Context.create_client_context()
    uri = context + "/.well-known/core"
    #print("\nCoap_Client: Discovering resources on {0}".format(uri))
    request = Message(code=GET, uri=uri)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print("Failed to discover resources on {0}".format(uri))
        print(e)
        calling_obj.response = None
        exit(-1)
    #pdb.set_trace()
    payload = str(response.payload)[2:-1]
    links = lh.parse(payload).links
    # Sorry, couldn't find a better way
    links = [(link.rt[0], link.get_target(context), link.code[0]) for link in links if 'rt' in link]
    res = {link[0]: uri_(link[1], link[2]) for link in links}
    if calling_obj:
        calling_obj.response = res
    #print("Coap Client: Discovered Resources: {0}\n".format(calling_obj.response))
    return res

async def _client_get(calling_obj, uri, payload):
    protocol = await Context.create_client_context()
    payload = bytes(payload, 'utf-8')
    request = Message(code=GET, uri=uri, payload=payload)
    #print("\n Coap Client: Request: GET {0} payload={1}".format(uri, payload))
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print("Failed while getting resource for uri= {0}, payload={1}".format(uri, payload))
        print(e)
        calling_obj.response = None
        exit(-1)
    payload = response.payload
    calling_obj.response = payload.decode('utf-8')
    #print("\n Coap Client: Response: {0}".format(calling_obj.response))


def coap_discover_resources(calling_obj=None, ip="localhost", port=COAP_PORT):
    asyncio.get_event_loop().run_until_complete(_coap_discover_resources(calling_obj, ip, port))


def coap_client_get(calling_obj, uri, payload):
    asyncio.get_event_loop().run_until_complete(_client_get(calling_obj, uri, payload))


if __name__ == "__main__":
    coap_discover_resources(ip="127.0.0.1", port=PATH_FINDER_SERVER_PORT)
    #coap_discover_resources()
