from __future__ import print_function
import json
import pdb
import socket

from CONSTANTS import *


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((HOST, SD_SERVER_PORT))
    while True:
        try:
            data, cl_addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            if PYTHON_VERSION == 3.5:
                data = data.decode('utf-8')
            print("SD Server received request from {0} data= {1}".format(cl_addr, data))
            request = json.loads(data)
            if request[SERVICE_KEY] == ALL_PATHS_FINDER_SERVICE:
                response = json.dumps({SERVICE_KEY: ALL_PATHS_FINDER_SERVICE,
                SERVICE_IP_ADDR: PATH_FINDER_SERVER_IP,
                SERVICE_PORT: PATH_FINDER_SERVER_PORT})
            elif request[SERVICE_KEY] == LIGHT_HISTORY_SERVICE:
                response = json.dumps({SERVICE_KEY: LIGHT_HISTORY_SERVICE,
                SERVICE_IP_ADDR: LIGHT_HISTORY_SERVER_IP,
                SERVICE_PORT: LIGHT_HISTORY_SERVER_PORT})
            else:
                print ("Unrecognized service request received {0}".format(request))
                continue
            #pdb.set_trace()
            if PYTHON_VERSION == 3.5:
                response = response.encode('utf-8')
            print("SD Server response = {0} ".format(response))
            sock.sendto(response, cl_addr)
        except Exception as e:
            print("Exception : {0}".format(e))

if __name__ == "__main__":
    main()