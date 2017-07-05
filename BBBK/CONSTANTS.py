import sys
from collections import namedtuple

PYTHON_VERSION = float(sys.version[:3])

HOST = ''                 # Symbolic name meaning all available interfaces
SD_CLIENT_PORT = 60000
SD_SERVER_PORT = 60010
SERVICE_KEY = "service_key"
SERVICE_IP_ADDR = "service_IP_addr"
SERVICE_PORT = "service_port"

_GET = "GET"
data_ = namedtuple("data", "lat, long, als, led, time")

IF_NAME = "wlan0"
LOCAL_NETWORK = '192.168.1.0/24'

LIVE_DATA = "live_data"
LOCALHOST = "127.0.0.1"


ALL_PATHS_FINDER_SERVICE = "AllPathsFinderService"
PATH_FINDER_SERVER_PORT = 60037
ALL_PATHS_RESOURCE = "allpaths"

LIGHT_HISTORY_SERVICE = "LightHistoryService"
LIGHT_HISTORY_SERVER_PORT = 60036
LIGHT_HISTORY_RESOURCE = "lightHistory"


port_mapping = {
    '192.168.1.51': 60001,
    '192.168.1.52': 60002,
    '192.168.1.53': 60003,
    '192.168.1.54': 60004
    }

CORE_ADDRESS = "152.14.87.22"
BROADCAST_ADDRESS = "192.168.1.255"
PATH_FINDER_SERVER_IP = "152.14.87.22"
LIGHT_HISTORY_SERVER_IP = "152.14.87.22"

# TODO : Uncomment the below lines.
#CORE_ADDRESS = "127.0.0.1"
#BROADCAST_ADDRESS = "127.0.0.1"
#PATH_FINDER_SERVER_IP = CORE_ADDRESS
#LIGHT_HISTORY_SERVER_IP = CORE_ADDRESS
