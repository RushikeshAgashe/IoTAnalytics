import csv
with open('New_file.csv') as f:
    data=[tuple(line) for line in csv.reader(f)]

print data
print len(data)
