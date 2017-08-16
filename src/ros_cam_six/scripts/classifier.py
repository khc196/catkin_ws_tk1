#!/usr/bin/env python
import sys
import rospy
import cv2
import tensorflow as tf
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

imagePath = '/home/sangwon1/catkin_ws/sign.jpg'
modelFullPath = '/home/sangwon1/output_graph.pb'
labelsFullPath = '/home/sangwon1/output_labels.txt'



def create_graph():
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image():
    answer = None

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()
    create_graph()



   
    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1] 
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))

        answer = labels[top_k[0]]
        return answer

class classifier:
    def __init__(self):
	self.bridge=CvBridge()
	self.image_sub= rospy.Subscriber("traffic_sign",Image,self.callback)
        
    def callback(self,data):
	try:
	    cv_image=self.bridge.imgmsg_to_cv2(data,"bgr8")
	except CvBrdigeError as e:
	    print(e)
        cv2.imwrite("sign.jpg" , cv_image)
        run_inference_on_image()


def main(args):
    heybro= classifier()
    rospy.init_node('classifier', anonymous=True)
    try:
	rospy.spin()
    except KeyboardInterrupt:
	print("shut down")
    cv2.destroyAllWindows()



if __name__ == '__main__': 


    main(sys.argv)


