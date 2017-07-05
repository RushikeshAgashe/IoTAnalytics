"""
This will run on core cloud. This asks all the user nodes for sensor data.
"""

import socket
import time
import json
import pdb

from CONSTANTS import PYTHON_VERSION, SD_CLIENT_PORT, SD_SERVER_PORT, LOCALHOST, LIVE_DATA, SERVICE_KEY
from CONSTANTS import data_


def send_request(request, multiple_response):
    cl_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cl_sock.settimeout(5.0)
    cl_sock.bind(('', SD_CLIENT_PORT))
    # Send to localhost, scapy sniffing on localhost
    # will forward to all edge nodes
    cl_sock.sendto(request, ('8.8.8.8', SD_SERVER_PORT))
    t_end = time.time() + 5
    response = []
    while time.time() < t_end:
        try:
            data, addr = cl_sock.recvfrom(1024)
            response.append((data, addr))
            if multiple_response is False:
                break
        except Exception as e:
            print("Exception : {0}".format(e))
            return response if response else None
    cl_sock.close()
    return response


def get_live_sensor_data(service_key=LIVE_DATA, multiple_response=True):
    req = json.dumps({SERVICE_KEY: service_key})
    if PYTHON_VERSION == 3.5:
        req = req.encode('utf-8')  # Comment out this line for python 2.7
    print("Polling Client asking for live data {0}".format(service_key))
    response = send_request(req, multiple_response)

    if PYTHON_VERSION == 3.5 and response:
        decoded_response = []
        for res in response:
            decoded_response.append((data_(*json.loads(res[0].decode('utf-8'))), res[1]))
        response = decoded_response
    print("Polling client Received response = {0}".format(response))
    return response

if __name__ == "__main__":
    while True:
        resp = get_live_sensor_data()
        time.sleep(5)
