import csv

graph = {}
with open('./csv/adjacency.csv') as f:
    for line in csv.reader(f):
        graph[line[0]] = set(line[1:])


coords = {}
with open('./csv/map_vertices_coordinates.csv') as f:
   for coord, x, y in csv.reader(f):
       coords[coord] = [float(x), float(y)]
   #print (coords)    
    
def allpathsfinderservice(start, end):
    paths = list(dfs_paths(graph, start, end))
    coord_paths = []
    for path in paths:
        coord_paths.append([coords[x] for x in path])
    #print (coord_paths)
    return coord_paths

def dfs_paths(graph, start, end):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == end:
                yield path + [next]
            else:
                stack.append((next, path + [next]))
       #vertices=[line for line in csv.reader(f)]

if __name__=="__main__":
    #pass
    allpathsfinderservice("A","G")
#    data = list(dfs_paths(graph, start, end))
#    print data
#    with open('All_Paths.csv','wb') as out:
#        csv_out=csv.writer(out)
#        for row in data:
#            csv_out.writerow(row)

#print graph['U']
