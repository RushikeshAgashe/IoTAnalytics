import random
from LightRetrieval import get_link_averages

def historyservice(list_of_paths):
    #lights = []
    #for path in list_of_paths:
    #    lights.append(random.randint(0, 100))
    #return lights
    return get_link_averages(list_of_paths, 604)
