#!/usr/bin/env python
import sys
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point

class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.imagecb)
    self.image_pub = rospy.Publisher("center_point",Point,queue_size=10)


  def imagecb(self,data):
    # Convert Image message to CV image with blue-green-red color order (bgr8)
    # create trackbars for color change
    # cv2.namedWindow('Converted Image')
    # cv2.createTrackbar('Lower Hue','Converted Image',0,180,nothing)
    # cv2.createTrackbar('Lower Sat','Converted Image',0,255,nothing)
    # cv2.createTrackbar('Lower Value','Converted Image',0,255,nothing)
    # cv2.createTrackbar('Upper Hue','Converted Image',0,180,nothing)
    # cv2.createTrackbar('Upper Sat','Converted Image',0,255,nothing)
    # cv2.createTrackbar('Upper Value','Converted Image',0,255,nothing)

    # lowh = cv2.getTrackbarPos('Lower Hue','Converted Image')
    # lows = cv2.getTrackbarPos('Lower Sat','Converted Image')
    # lowv = cv2.getTrackbarPos('Lower Value','Converted Image')
    # upph = cv2.getTrackbarPos('Upper Hue','Converted Image')
    # upps = cv2.getTrackbarPos('Upper Sat','Converted Image')
    # uppv= cv2.getTrackbarPos('Upper Value','Converted Image')
    try:

      # create switch for ON/OFF functionality
      # switch = '0 : OFF \n1 : ON'
      # cv2.createTrackbar(switch, 'Converted Image',0,1,nothing)



      lower_red = np.array([0,180,125])
      upper_red = np.array([10,255,255])

      img_original = self.bridge.imgmsg_to_cv2(data, "bgr8")
      img_original = cv2.flip(img_original,1)
      hsv = cv2.cvtColor(img_original,cv2.COLOR_BGR2HSV)
      # lower_red = np.array([lowh,lows,lowv])
      # upper_red = np.array([upph,upps,uppv])
      mask = cv2.inRange(hsv,lower_red, upper_red)
      print mask[2,2]
      res =cv2.bitwise_and(img_original,img_original,mask= mask)


      contour = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
      center = None

      if len(contour) > 0:
        c = max(contour, key = cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if radius > 30:
          center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # else:
        #   center = (0,0)
          res = cv2.circle(res,(int(center[0]),int(center[1])),int(radius),(0,255,0),2)
          img_original = cv2.circle(img_original,(int(center[0]),int(center[1])),int(radius),(0,255,0),2)

          #print center
          self.image_pub.publish(center[0],center[1],0)

      cv2.imshow("Converted Image",np.hstack([img_original,res]))

      cv2.waitKey(3)
    except CvBridgeError, e:
      print("==[CAMERA MANAGER]==", e)

def nothing(x):
  pass

def main():
  rospy.init_node('image_converter', anonymous=True)
  ic = image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
  print "Image Converter is Running"
  main()
