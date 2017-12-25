#!/usr/bin/env python
import serial
import time
from scipy.interpolate import interp1d
import rospy
from geometry_msgs.msg import Point
global sx
global sy
sx = 0
sy = 0

class point_process:

    def __init__(self):
        self.point_sub = rospy.Subscriber("center_point",Point,self.pointcb)

    def pointcb(self,data):
        global sx
        global sy

        lowx = -320
        highx = 320

        lowy = 0
        highy = 480

        center = data
        x = int(center.x)
        y = int(center.y)
        mx = interp1d([0,620],[lowx,highx],bounds_error=False)
        my = interp1d([0,480],[highy,lowy],bounds_error=False)

        x = mx(x)
        y = my(y)
        #print x,y-200
        delt = 8

        if (sx < highx+1 and sx > lowx-1) and abs(x) > 40:
            if (x - 0 > 0 ) and sx < highx-delt+1:
                deg2servo(0,sx+delt)
                sx += delt
                time.sleep(.003)
            if (x - 0 < 0) and sx > lowx+delt-1:
                deg2servo(0,sx-delt)
                sx -= delt
                time.sleep(.003)
        if (sy < highy+1 and sy > lowy-1) and abs(y-200) > 40:
            if (y - 0 > highy/2 ) and sy < highy-delt+1:
                deg2servo(1,sy+delt)
                time.sleep(.003)
                sy += delt
            if (y - 0 < highy/2) and sy > lowy+delt-1:
                deg2servo(1,sy-delt)
                sy -= delt
                time.sleep(.003)

def deg2servo (port,angle):
    lowx = -320
    highx = 320

    lowy = 0
    highy = 480
    if port == 0:
        m = interp1d([highx,lowx],[992,2000])
        port = 0x00
    else:
        m = interp1d([lowy,highy],[992,2000])
        port = 0x01

    convNum = m(angle)

    with serial.Serial('/dev/ttyACM0',baudrate=9600,timeout=1) as ser:
        a = bin(int(convNum*4))
        lena = len(a) - 2
        firstNum = lena - 7
        tbyte = '0'+a[2:2+firstNum]
        sbyte = a[-7:]
        ser.write(chr(0x84)+chr(port)+chr(int(sbyte,2))+chr(int(tbyte,2)))

def cirCount(count):

    deg2servo(0,-45)
    time.sleep(1)
    deg2servo(1,0)
    time.sleep(1)

    for j in range(count):
        for i in range (0,90,1):
            deg2servo(0,i-45)
            time.sleep(.001)
        for i in range (0,90,1):
            deg2servo(1,i)
            time.sleep(.001)
        for i in range(90,0,-1):
            deg2servo(0,i-45)
            time.sleep(.001)
        for i in range (90,0,-1):
            deg2servo(1,i)
            time.sleep(.001)

def main():
    global sx
    global sy
    rospy.init_node('point_process')
    pcenter = point_process()
    try:
        deg2servo(0,0)
        time.sleep(1)
        deg2servo(1,0)
        time.sleep(1)
        # sx = 0
        # sy = 0
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
