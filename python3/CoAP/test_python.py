from client import *
import logging
import asyncio

from aiocoap import *

asyncio.get_event_loop().run_until_complete(client_function_get())
