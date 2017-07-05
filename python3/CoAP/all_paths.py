import csv

start = 'N'
end = 'A'

vertices = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
graph = {}
with open('./adjacency.csv') as f:
    for line in csv.reader(f):
        graph[line[0]] = set(line[1:])


def dfs_paths(graph, start, end):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == end:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

all_paths = list(dfs_paths(graph, start, end))
print(all_paths)

########################### "All_Paths.csv" is an ___OUTPUT file___ ########
##
##with open('All_Paths.csv','wb') as out:
##    csv_out=csv.writer(out)
##    for row in all_paths:
##        csv_out.writerow(row)

####### "path_vertices_coordinates.csv" is an _____INPUT file______#######

with open('map_vertices_coordinates.csv') as f:
    coordinatesWithVertex = [list(line) for line in csv.reader(f)]

coordinateDict = {d[0]: d[1:] for d in coordinatesWithVertex}

all_coordinates = []
for i in range(0,len(coordinatesWithVertex)):
    all_coordinates.append(coordinatesWithVertex[i][1:])

for i in range(0,len(all_coordinates)):
    x,y = all_coordinates[i]
    all_coordinates[i] = [float(x),float(y)]

i = 0
for d in vertices:
    coordinateDict[d] = all_coordinates[i]
    i = i+1

path_coordinates = []
temp = []

for i in range (0,len(all_paths)):
    for j in range (0,len(all_paths[i])):
        temp.append(coordinateDict[all_paths[i][j]])
        #print temp , 'TEMP'
    path_coordinates.append(temp)
    temp = []

############### "all_paths_coordinates.csv" is an ___OUTPUT file___ ########

with open('all_paths_coordinates.csv','w') as out:
    csv_out=csv.writer(out)
    for row in path_coordinates:
        csv_out.writerow(row)
#print path_coordinates



## all_paths_coordinates.csv to UserApplication
