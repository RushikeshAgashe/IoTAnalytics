from services.paths_service import allpathsservice
from services.history_service import historyservice


def service_discovery_request(service_key):
    if service_key in sample_services:
        return sample_services[service_key]
    else:
        return None

def connected(service):
    return True

def send(service, args):
    if service == "0.0.0.0/allpaths":
        paths = allpathsservice(args["start"], args["end"])
        return paths

    elif service == "0.0.0.0/history":
        lights = historyservice(args["paths"])
        return lights

    else:
        raise NotImplementedError()

sample_services = {
    "allpaths" : "0.0.0.0/allpaths",
    "history" : "0.0.0.0/history",
    "cluster" : "0.0.0.0/cluster",
    "orderpizza" : "0.0.0.0/papajohns",
    "killallhumans" : "0.0.0.0/nuclear"
}
