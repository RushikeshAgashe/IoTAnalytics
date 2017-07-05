from __future__ import print_function
import json
import time
import pdb
import socket
import subprocess
from CONSTANTS import PYTHON_VERSION, SERVICE_KEY, HOST, SD_SERVER_PORT
from CONSTANTS import data_, LIVE_DATA


def read_gps_value():
    return subprocess.run("/root/uart_gps/GetGPSData", stdout=subprocess.PIPE).stdout.decode('utf-8').split()


def read_als_value():
     return subprocess.run(["/root/uart_gps/als_read", "2", "200", "none"], stdout=subprocess.PIPE).stdout.decode('utf-8').split()


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
            if request[SERVICE_KEY] == LIVE_DATA:
                # TODO: Read the actual sensor values
                lat, long, time = read_gps_value()
                als, led, _ = read_als_value()
                resp = data_(lat, long, als, led, time)
                resp = json.dumps(resp)
            else:
                print("Unrecognized service request received {0}".format(request))
                continue

            if PYTHON_VERSION == 3.5:
                resp = resp.encode('utf-8')
            print("SD server response = {0}".format(resp))
            sock.sendto(resp, cl_addr)
        except Exception as e:
            print("Exception : {0}".format(e))


if __name__ == "__main__":
    main()

