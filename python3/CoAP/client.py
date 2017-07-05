#!/usr/bin/env python3

import logging
import asyncio
import pickle
from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def client_function_put(payload):
    context = await Context.create_client_context()

    await asyncio.sleep(2)

    #payload = b"The quick brown fox jumps over the lazy dog.\n" * 30
    payload = bytes(payload, 'utf-8')
    request = Message(code=PUT, payload=payload)
    request.opt.uri_host = '127.0.0.1'
    request.opt.uri_path = ("other", "block")

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload))



async def client_function_get():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://localhost/lightdata')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        payload = response.payload
        payload = payload.decode('utf-8')
        print('Result: %s\n%r'%(response.code, payload))
        print(payload)

