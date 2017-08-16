# -*- coding: utf8 -*-
#!/usr/bin/python
import socket
import cv2
import numpy

TCP_IP = '192.168.117.1'
TCP_PORT = 60000

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

capture = cv2.VideoCapture(0)
while(capture.isOpened()) :
	ret, frame = capture.read()
	if not ret :
	  continue

	encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
	result, imgencode = cv2.imencode('.jpg', frame, encode_param)
	data = numpy.array(imgencode)
	stringData = data.tostring()

	sock.send(unicode(str(len(stringData)).ljust(16), "utf-8"));
	sock.send(stringData);
	decimg=cv2.imdecode(data,1)
	cv2.imshow('CLIENT',decimg)
	cv2.waitKey(3)
sock.close()
cv2.destroyAllWindows() 
