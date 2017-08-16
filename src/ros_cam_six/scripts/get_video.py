#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError



def image_publisher():
    video=rospy.Publisher("ros_cam_six",Image, queue_size=10)
    rospy.init_node('get_video', anonymous=True)
    rate=rospy.Rate(10)
    
    cam=cv2.VideoCapture(0)
    cv2. waitKey(3)

    

    while not rospy.is_shutdown():
	ret,frame=cam.read()
	cv2.imshow('output', frame)
	#msg_frame=CvBridge().cv2_to_imgmsg(frame,"bgr8")
	#video.publish(msg_frame)
	rate.sleep()
    cam.release()
    cv2.destroyAllWindows()




if __name__ == '__main__':
    try:
        image_publisher()
    except rospy.ROSInterruptException:
        pass




