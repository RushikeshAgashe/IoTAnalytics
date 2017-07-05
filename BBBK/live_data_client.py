import socket
import time
import json
import pdb

from CONSTANTS import LIVE_DATA, SERVICE_KEY, PYTHON_VERSION, SD_CLIENT_PORT, BROADCAST_ADDRESS, SD_SERVER_PORT


def send_request(request, multiple_response):
    cl_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cl_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cl_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    cl_sock.settimeout(5.0)
    cl_sock.bind(('', SD_CLIENT_PORT))
    # TODO: BROADCAST_ADDRESS delete
    #BROADCAST_ADDRESS = "127.0.0.1"  # To test at local host
    cl_sock.sendto(request, (BROADCAST_ADDRESS, SD_SERVER_PORT))
    t_end = time.time() + 5
    response = []
    while time.time() < t_end:
        try:
            data, addr = cl_sock.recvfrom(1024)
            response.append((data, addr))
            if multiple_response is False:
                break
        except Exception as e:
            print("Exception: {0}".format(e))
            return response if response else None
    cl_sock.close()
    return response

def get_live_sensor_data(service_key=LIVE_DATA, multiple_response=True):
    req = json.dumps({SERVICE_KEY: service_key})
    if PYTHON_VERSION == 3.5:
        req = req.encode('utf-8')
    print("Live Data client requesting for for {0}".format(service_key))
    response = send_request(req, multiple_response)
    if PYTHON_VERSION == 3.5 and response:
        decoded_response = []
        for res in response:
            decoded_response.append((json.loads(res[0].decode('utf-8')), res[1]))
        response = decoded_response
    print("Live Data Client Received response = {0}".format(response))
    return response

if __name__ == "__main__":
    get_live_sensor_data()
