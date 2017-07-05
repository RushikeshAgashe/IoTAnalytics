import json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


# Completed
def sd_request_to_json(skey_req_parameters):
    new_param = Object()
    new_param.service_key = skey_req_parameters
    return new_param.toJSON()

# Completed
def sd_response_to_json(service_ip_addr_param, service_port_param, skey_param):
    new_param = Object()
    new_param.service_IP_addr = service_ip_addr_param
    new_param.service_port = service_port_param
    new_param.service_key = skey_param
    return new_param.toJSON()

# Completed
def all_paths_finder_service_request_to_json(src, dest):
    new_param = Object()
    new_param.source = src
    new_param.destination = dest
    return new_param.toJSON()

# Completed
def all_paths_finder_service_response_to_json(path_list_response):
    new_param = Object()
    new_param.path_list = path_list_response
    return new_param.toJSON()

# Completed
def light_history_service_request_to_json(path_list_req, time_stamp_req):
    new_param = Object()
    new_param.path_list = path_list_req
    new_param.time_stamp = time_stamp_req
    return new_param.toJSON()

# Completed
def light_history_service_response_to_json(light_hist_list_resp, unit_resp="lux"):
    new_param = Object()
    new_param.light_hist_list = light_hist_list_resp
    new_param.unit = unit_resp
    return new_param.toJSON()

# Completed
def collect_live_sensor_data_request_to_json(requester_type_req, requested_data, requested_ts):
    new_param = Object()
    new_param.requester_type = requester_type_req
    new_param.requested_data = requested_data
    new_param.time_stamp = requested_ts
    return new_param.toJSON()

# Completed
def collect_live_sensor_data_response_to_json(light_level_resp, coordinates_resp, timestamp_collected_resp, unit_resp = "lux"):
    new_param = Object()
    new_param.light_level = light_level_resp
    new_param.coordinates = coordinates_resp
    new_param.timestamp_collected = timestamp_collected_resp
    new_param.unit = unit_resp
    return new_param.toJSON()


#TEST: Print out JSON format
# Float array
source = [44.968046,   -94.420307]
destination = [44.33328,    -89.132008]

#3d Array
path_list = [[[12.23,13.54], [14.11,15.32], [483.232, 7574.78]],
             [[12.23, 13.54], [14.11, 15.32], [483.232, 7574.78]],
             [[12.23, 13.54], [14.11, 15.32], [483.232, 7574.78]]
             ]
# Time Stamp
ts = "04/19/2017 12:00:32PM"
# Light history
hist_list = [[2,3], [5,6], [7, 8]]



# print (cv["service_key"])
# Test Method 2
#print(sd_response_to_json("192.168.1.1", 80, "path_finder"))
# Test Method 3
#print(all_paths_finder_service_request_to_json(source, destination))

# Test Method 4
#print(all_paths_finder_service_response_to_json(path_list))

# Test Method 5
# print(light_history_service_request_to_json(path_list, ts))

# Test Method 6
# print(light_history_service_response_to_json(hist_list))

# Test Method 7
# print(collect_live_sensor_data_request_to_json("core_cloud", "light_level", ts))

# Test Method 8
# print(collect_live_sensor_data_response_to_json(1432, source, ts))
