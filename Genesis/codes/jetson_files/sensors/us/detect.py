import os
import math
import ydlidar
import time
import sys
from functions import *

rancorr = 80 / 3.2
rad2deg = 180 / math.pi
deg2rad = math.pi / 180


port = "/dev/ydlidar"

laser = ydlidar.CYdLidar()
laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 128000)
laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TOF)
laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
laser.setlidaropt(ydlidar.LidarPropScanFrequency, 6.0)
laser.setlidaropt(ydlidar.LidarPropSampleRate, 5)
laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)
laser.setlidaropt(ydlidar.LidarPropMaxAngle, 90.0)
laser.setlidaropt(ydlidar.LidarPropMinAngle, -90.0)
laser.setlidaropt(ydlidar.LidarPropMaxRange, 4.0)
laser.setlidaropt(ydlidar.LidarPropMinRange, 0.01)


x_thresh = 30.0
y_thresh = 60.0

objr = None

def mov(r, theta, x_thresh, angle_thresh, move_direction):
    if x_thresh > r:
        return None

    curr = theta
    if move_direction == 'left':
        while abs(r * math.sin(deg2rad * curr)) < x_thresh:
            curr += 1
    else:
        while abs(r * math.sin(deg2rad * curr)) < x_thresh:
            curr -= 1

    #print(f'r:{r:.2f} theta:{theta:.2f} ang:{theta-curr}')
    return theta - curr

def detect(angle, ran):
    mmap = {}
    for idx, val in enumerate(ran):
        if val > 20.0:
            mmap[-angle[idx] * rad2deg] = val
    mmap = dict(sorted(mmap.items()))
    
    left = {}
    right = {}

    for ang in mmap.keys():
        x = mmap[ang] * math.sin(ang * deg2rad)
        y = mmap[ang] * math.cos(ang * deg2rad)
        if(abs(x) < x_thresh and abs(y) < y_thresh):
            if(ang > 0):
                right[ang] = mmap[ang]
            else:
                left[ang] = mmap[ang]
    '''
    print('left')
    for ang in left.keys():
        print(f'r:{left[ang]:.2f} ang:{ang:.2f}')
    print('right')
    for ang in right.keys():
        print(f'r:{right[ang]:.2f} ang:{ang:.2f}') 

    '''
    if len(list(left)) > len(list(right)):
        objr = False
    elif len(list(right)) > len(list(left)):
        objr = True
    else:
        objr = None

    if objr == True:
        objs = list(right)[0]
        obje = list(right)[-1]
        
        if len(list(left)) > 0:
            objs = list(left)[0]
    
    elif objr == False:
        objs = list(left)[-1]
        obje = list(left)[0]

        if len(list(right)) > 0:
            objs = list(right)[-1]
    
    if objr == True or objr == False:
       
        y_s = mmap[objs] * math.cos(deg2rad * objs)
        y_e = mmap[obje] * math.cos(deg2rad * obje)
        y_diff = y_s - y_e

        if objr:
            angle = mov(mmap[objs], objs, x_thresh, 5, 'left')
        else:
            angle = mov(mmap[objs], objs, x_thresh, 5, 'right')
        
        # Move reverse for one second
        if angle == None:
            print('R')

            #indent here
            stop()
            #time.sleep(1)
            move_backward()
            #time.sleep(1)
            
        # Takes 2 seconds to stop, then rotates and waits for 1second
        else:
            #indent here
            stop()
            #time.sleep(1)

            if(angle > 0):
                rotate(angle, 'right')
            else:
                rotate(-angle, 'left')
            #time.sleep(1)
            
            print(angle)
    # If no obstalce, move forward
    else:
        #indent here
        move_forward()

        print('F')
        
def animate(scan):
    r = laser.doProcessSimple(scan)
    if r:
        angle = []
        ran = []
        with open('data.txt', 'w') as file:
            for point in scan.points:
                dist = point.range * rancorr
                ang = point.angle
                angle.append(-ang)
                ran.append(dist)
                file.write(f'ang:{ang * rad2deg:.2f}, dist:{dist:.2f}\n')
            detect(angle, ran)

try:
    ret = laser.initialize()
    if ret:
        ret = laser.turnOn();
        scan = ydlidar.LaserScan()
        while ret and ydlidar.os_isOk() :
            r = laser.doProcessSimple(scan);
            if r:
                animate(scan)
        laser.turnOff();

    laser.disconnecting()
finally:
    stop()
