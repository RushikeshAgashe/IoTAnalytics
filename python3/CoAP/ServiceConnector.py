from paths_service import allpathsfinderservice
from history_service import lighthistoryservice
import JSON.service_schema_library_json as tojson
import JSON.service_schema_library_raw_data as toraw

def discover(message):
    request = toraw.sd_request_to_raw_dict(message)

    if "service_key" in request and request["service_key"] in sample_services:
        response = tojson.sd_response_to_json(*sample_services[request["service_key"]])
    else:
        response = None

    return response

def connected(service):
    return True

def send(destination, message):
    ip = destination["service_IP_addr"]
    port = destination["service_port"]
    key = destination["service_key"]

    if ip == "0.0.0.0" and port == "0":
        if key == "/allpaths":
            sd = toraw.all_paths_finder_service_request_to_raw_dict(message)
            paths = allpathsservice(sd["source"], sd["destination"])
            response = tojson.all_paths_finder_service_response_to_json(paths)
            return response

        elif key == "/history":
            paths = toraw.light_history_service_request_to_raw_dict(message)
            lights = historyservice(paths["path_list"]["path_list"], paths["time_stamp"])
            response = tojson.light_history_service_response_to_json(lights)
            return response

    raise NotImplementedError()

sample_services = {
    "allpaths" : ["0.0.0.0", "0", "/allpaths"],
    "history" : ["0.0.0.0", "0", "/history"],
    "cluster" : ["0.0.0.0", "0", "/cluster"],
    "orderpizza" : ["0.0.0.0", "0", "/papajohns"],
    "killallhumans" : ["0.0.0.0", "0", "/nuclear"]
}
