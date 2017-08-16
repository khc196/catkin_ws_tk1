#!/usr/bin/env python

import rospy
from race.msg import drive_param
import curses
from socket import *
from select import select
import sys
from time import sleep
#import signal
#TIMEOUT = 0.1 # number of seconds your want for timeout
forward = 0;
left = 0;

HOST = '192.168.117.1'
PORT = 50000
BUFSIZE = 1024
ADDR = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)

try:
	clientSocket.connect(ADDR)
except Exception as e:
	sys.exit()

def prompt():
	sys.stdout.flush()

rospy.init_node('g29_talker', anonymous=True)
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)
while(True) :
	try:
		connection_list = [sys.stdin, clientSocket]
		read_socket, write_socket, error_socket = select(connection_list, [], [], 10)
		for sock in read_socket:
			if sock == clientSocket:
				data = sock.recv(BUFSIZE)
				if not data:
					clientSocket.close()
					sys.exit()
				else:
					convert = data.split('\x00')
					result = float(convert[0])
					print(result)
					msg = drive_param()
					msg.velocity = 0
					msg.angle = result / 32767 * 85
					pub.publish(msg)
					sleep(0.005)
					prompt()
			else:
				prompt()	
	except KeyboardInterrupt:
		clientSocket.close()
		sys.exit()
curses.endwin()
