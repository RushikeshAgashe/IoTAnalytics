import csv

graph = {}
with open('./csv/adjacency.csv') as f:
    for line in csv.reader(f):
        graph[line[0]] = set(line[1:])

coords = {}
with open('./csv/map_vertices_coordinates.csv') as f:
   for coord, x, y in csv.reader(f):
       coords[coord] = [float(x), float(y)]
    
def allpathsfinderservice(startcoord, endcoord):
    start, end = getclosest(*startcoord), getclosest(*endcoord)

    paths = list(dfs_paths(graph, start, end))
    coord_paths = []
    for path in paths:
        coord_paths.append([coords[x] for x in path])
    return coord_paths

#TODO: get closest to start and end
def getclosest(lng, lat):
    for c in coords:
        lng2, lat2 = coords[c]
        if lng2 == lng and lat2 == lat:
            return c

def dfs_paths(graph, start, end):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == end:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

if __name__=="__main__":
    allpathsfinderservice("A","G")
