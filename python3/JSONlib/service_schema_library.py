
import json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

 # Serialize to JSON


def sd_request_to_json(req_parameters):
    new_param = Object()
    new_param.service_key = req_parameters
    return new_param.toJSON()


def all_paths_finder_service_to_json(source, destination):
    new_param = Object()
    new_param.source = source
    new_param.destination = destination
    return new_param.toJSON()

def light_history_service_to_json(route_list, time_stamp):
    new_param = Object()
    new_param.route_list = route_list
    new_param.time_stamp = time_stamp
    return new_param.toJSON()

def data_request_to_json(requester_type, requested_data):
    new_param = Object()
    new_param.requester_type = requester_type
    new_param.requested_data = requested_data
    return new_param.toJSON()

def data_response_service_to_json(light_level, way_point, timestamp_collected, unit):
    new_param = Object()
    new_param.light_level = light_level
    new_param.way_point = way_point
    new_param.timestamp_collected = timestamp_collected 
    new_param.unit = unit
    return new_param.toJSON()


#TEST: Print out JSON format

source = [44.968046,   -94.420307]
destination = [44.33328,    -89.132008]
# Test Method 1
print(sd_request_to_json("light_history_service"))
# Test Method 2
print(all_paths_finder_service_to_json(source, destination))


# TODO
# 1. Test serialization for all methods
# 2. Deserialize all service response from Server
