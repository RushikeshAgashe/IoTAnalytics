import json

def sd_request_to_raw_dict(jsonObject):
    dictionary = json.loads(jsonObject)
    return dictionary

def sd_response_to_raw_dict(jsonObject):
    dictionary = json.loads(jsonObject)
    return dictionary

def all_paths_finder_service_request_to_raw_dict(jsonObject):
    dictionary = json.loads(jsonObject)
    return dictionary

def all_paths_finder_service_response_to_raw_dict(jsonObject):
    dictionary = json.loads(jsonObject)
    return dictionary

def light_history_service_request_to_raw_dict(jsonObject):
    dictionary = json.loads(jsonObject)
    return dictionary

def light_history_service_response_to_raw_dict(jsonObject):
    dictionary = json.loads(jsonObject)
    return dictionary

def collect_live_sensor_data_request_to_raw_dict(jsonObject):
    dictionary = json.loads(jsonObject)
    return dictionary

def collect_live_sensor_data_response_to_raw_dict(jsonObject):
    dictionary = json.loads(jsonObject)
    return dictionary


# Test Method 1
# jsonObject = (sd_request_to_json("light_history"))
# dic = sd_request_to_raw_dict(jsonObject)
#print(dic["service_key"])

# Test Method 2
# jsonObject = sd_response_to_json("192.168.1.1", 80, "path_finder")
# dic = sd_response_to_raw_dict(jsonObject)
# # print(dic["service_IP_addr"], "\n", dic["service_port"], "\n", dic["service_key"] )
#
# jsonObject = all_paths_finder_service_request_to_json(source, destination)
# dic = all_paths_finder_service_request_to_raw_dict(jsonObject)
# #print(dic["source"],"\n", dic["destination"] )
#
# jsonObject = all_paths_finder_service_response_to_json(path_list)
# dic= all_paths_finder_service_response_to_raw_dict(jsonObject)
# # print(dic["path_list"])
#
# jsonObject = light_history_service_request_to_json(path_list, ts)
# dic = light_history_service_request_to_raw_dict(jsonObject)
# # print(dic["path_list"], "\n", dic["time_stamp"])
#
# jsonObject = light_history_service_response_to_json(hist_list)
# dic = light_history_service_response_to_raw_dict(jsonObject)
# # print(dic["light_hist_list"], "\n", dic["unit"])
#
# jsonObject = collect_live_sensor_data_request_to_json("core_cloud", "light_level", ts)
# dic = collect_live_sensor_data_request_to_raw_dict(jsonObject)
# #print(dic["requester_type"], "\n", dic["requested_data"], "\n", dic["time_stamp"])
#
# jsonObject = collect_live_sensor_data_response_to_json(1432, source, ts)
# dic = collect_live_sensor_data_response_to_raw_dict(jsonObject)
# print(dic["light_level"], "\n", dic["coordinates"], "\n", dic["timestamp_collected"], "\n", dic["unit"])
