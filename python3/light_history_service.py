import math
import csv
import ast
import sqlite3

database = 'RandomData.db'

def conv_to_int(list):
    new_list = []
    for i in range(0, len(list)):
        for j in range(0, len(list[i])):
            new_list.append(eval(list[i][j]))
        list[i] = new_list;
        new_list = []
    return list

def read_from_db(db, time, output):
    temp = 0
    temp2 = []
    db.execute("SELECT ambientlight FROM AmbientLight WHERE timesegment=(?) AND link = (?)", (time, output))
    for line in db.fetchall():
        temp = temp + 1
        temp2.append(line[0])
    return temp2

## Will be taken from User input ##
timesegment = str(604).zfill(4)
with open('./csv/all_paths_coordinates.csv') as f:
   all_paths_coordinates=[line for line in csv.reader(f)]

## STATIC RESOURCE FILE ##
with open('./csv/map_vertices_coordinates.csv') as f:
   vertices=[line for line in csv.reader(f)]

vertexpoints = []
for i in range(0, len(vertices)):
    vertexpoints.append(vertices[i][1:])

all_paths_coordinates = conv_to_int(all_paths_coordinates)
vertexpoints = conv_to_int(vertexpoints)

def get_link_averages(all_paths, time):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    all_linkaverages = []

    for path in all_paths:
        linkaverages = []
        for i in range(0,len(path)-1):
            first = vertices[vertexpoints.index(path[i])][0]
            second = vertices[vertexpoints.index(path[i+1])][0]

            outputstring = ''.join(sorted(str(first)+str(second)))
            lightvalues = read_from_db(c, time, outputstring)

            average = sum(lightvalues)/len(lightvalues) if (sum(lightvalues) > 0) else (sum(lightvalues))
            linkaverages.append(average)

        all_linkaverages.append(linkaverages)
    print (all_linkaverages)
    #print all_paths_coordinates[alllinkaverages.index(max(alllinkaverages))]
    return all_linkaverages

if __name__ == "__main__":
    get_link_averages(all_paths_coordinates, timesegment)
