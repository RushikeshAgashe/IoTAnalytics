from __future__ import print_function

from collections import Counter, deque
import sys
import time

import numpy as np

try:
    from sklearn import neighbors, svm
    HAVE_SK = True
except ImportError:
    HAVE_SK = False

from common import *
from myo_raw import MyoRaw
from myo import *



#----------- Main Function -------------------#

if __name__ == '__main__':
    import subprocess
    m = Myo(NNClassifier(), None)
    m.add_raw_pose_handler(print)

    def page(pose):
        if pose == 5:
            subprocess.call(['xte', 'key Page_Down'])
        elif pose == 6:
            subprocess.call(['xte', 'key Page_Up'])

    m.add_raw_pose_handler(page)

    m.connect()

    vibrate = int(sys.argv [1])
    
    def wrongturn():
        for i in range (0,10):
            m.vibrate(3)
        vibrate = 0
        sys.exit(0)
        
    def left():
        for i in range (0,3):
            m.vibrate(2)
        vibrate = 0
        sys.exit(0)    
    def right():
        for i in range (0,6):
            m.vibrate(1)
        vibrate = 0
        sys.exit(0)    
    def reached():
        for i in range (0,5):
            m.vibrate(1)
            m.vibrate(2)
        vibrate = 0
        sys.exit(0)
        
    def dont_do_anything():
        m.vibrate(0)
        sys.exit(0)    
            
    while True:
        if vibrate == -2:
            vibrate = 0
            wrongturn()
           
        elif vibrate == -1:
            vibrate = 0
            left()
           
        elif vibrate == 1:
            vibrate = 0
            right()
           
        elif vibrate == 2:
            vibrate = 0
            reached()
           
        else:
            dont_do_anything()
    