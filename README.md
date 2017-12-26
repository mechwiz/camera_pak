## Camera Ball Tracker
**Michael Wiznitzer**

Northwestern University MSR Hackathon (Fall 2017)

## Introduction
#### Objective
To track a red ball with a camera mounted on 2 servos that are commanded to move such that the ball stays in the center of the camera frame.

#### Ball Tracking
The ROS camera driver used to get a live video feed is supported by the [usb_cam](http://wiki.ros.org/usb_cam) package. Once a feed is obtained, each image is converted to the HSV color space for better color segmentation using OpenCV. The upper and lower HS bounds for the red color were determined experimentally and can be adjusted using trackbars if need be to take into account different lighting conditions. The centroid of the largest contour in each filtered image is determined and is passed along to the servo node.

#### Servo Control
With the centroid information passed to this node, the servos can be controlled such that the centroid is always in the center of the camera frame. The servos are mounted on a [pan-tilt mechanism](https://www.sparkfun.com/datasheets/Robotics/Other/sensor%20pan%20tilt%20manual.jpg) and are controlled through the [Pololu Micro Maestro servo controller](https://www.pololu.com/docs/0J40/1.a). For smooth motion, each servo position is updated with a small increment or decrement followed by a very small time delay.

## Implementation
#### Launch
[`camera_trak.launch`](launch/camera_trak.launch)

#### Nodes
##### Ball Tracking Node
[`camera_pak_node.py`](nodes/camera_pak_node.py)

Subscribed Topic: `/usb_cam/image_raw`

Published Topic: `/center_point`

##### Servo Control Node
[`servotrack_node.py`](launch/servotrack_node.py)

Subscribed Topic: `/center_point`

## Demo
#### GIF Video
A video of the ball tracking in action can be seen below.

![balltracker.gif](imgs/balltracker.gif)
