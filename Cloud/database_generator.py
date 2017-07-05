import sqlite3
import csv
import os.path
from random import randint

#database = 'AmbientLightStorage.db'
database = 'RandomData.db'
conn = sqlite3.connect(database)
lightmodels = {'RANDOM': randint(0,255), 'ZEROINITIALIZED': 0}
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS AmbientLight(gpsvalue TEXT, timesegment TEXT, link TEXT, ambientlight INTEGER)")
    conn.commit()

def dynamic_data_entry():
    c.execute("INSERT INTO AmbientLight(gpsvalue, timesegment, link, ambientlight) VALUES (?, ?, ?, ?)",
          (gpsvalue, timesegment, link, ambientlight))
    

def close_database():
    conn.commit()
    c.close()
    conn.close()

links = ['AB','BC','CD','DE','EF','FG','FH','HM','IJ','IN','JK','BK','KL','DM','IM','NO','CO']
ambientlight = 0
gpsvalue = 0

create_table()
startTime = 0
endTime = 2400
time = startTime
#lightmodel = lightmodels['ZEROINITIALIZED']
#lightmodel = lightmodels['RANDOM']()

print("STARTED")
while time < endTime:
    for k in range (0,17):
        link = links[k]
        path = os.path.join('./Links/'+link+'.csv')
        
        with open(path) as f:
           gpslist=[line for line in csv.reader(f)]
        
        for i in range (time//2, time//2+30):
            timesegment = str(i*2).zfill(4)
            for j in range (0, len(gpslist)):
                #ambientlight = lightmodel
                ambientlight = randint(0,255)
                gpsvalue = repr(gpslist[j])
                dynamic_data_entry()
    
    time = time + 100
close_database()
print("COMPLETED filling database ---->  " + database)
#print("All values initialized to " + 'ZEROINITIALIZED')
print ("All values initialized to " + 'RANDOM')
