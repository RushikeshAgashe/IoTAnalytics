from __future__ import print_function
import socket
import time
import json
import pdb
from CONSTANTS import *


def send_request(request, multiple_responses):
    """
    :param request:
    :param multiple_responses:
    :return: A list of tuples. The tuples shall be (data, addr)
    """
    cl_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cl_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cl_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    cl_sock.settimeout(5.0)
    cl_sock.bind(('', SD_CLIENT_PORT))
    cl_sock.sendto(request, (BROADCAST_ADDRESS, SD_SERVER_PORT))
    t_end = time.time() + 5
    response = []
    while time.time() < t_end:
        try:
            data, addr = cl_sock.recvfrom(1024)
            response.append((data, addr))
            if not multiple_responses:
                break
        except Exception as e:
            print("Exception : {0}".format(e))
            return None
    return response


def discover_service(service_key):
    req = json.dumps({SERVICE_KEY: service_key})
    if PYTHON_VERSION == 3.5:
        req = req.encode('utf-8')  # Comment out this line for python 2.7
    print("SD client Discovering Service for {0}".format(service_key))
    response = send_request(req, False)
    decoded_response = []
    if PYTHON_VERSION == 3.5 and response:
        #pdb.set_trace()
        for res in response:
            decoded_response.append((json.loads(res[0].decode('utf-8')), res[1]))
            response = decoded_response
    print("SD Client Received response response = {0}".format(response))
    return response


def discover_all_paths_finder_service():
    response = discover_service(ALL_PATHS_FINDER_SERVICE)
    return response

def discover_history_service():
    response = discover_service(LIGHT_HISTORY_SERVICE)
    return response

if __name__ == "__main__":
    discover_all_paths_finder_service()
    discover_history_service()