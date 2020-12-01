
from  socket import timeout
import socket
import sys
import time
from check import ip_checksum
import random
import select
import Queue

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inputs = [s]
outputs= [s]
timeout = 1


host='localhost'
port = 9999 
print type(port) 
s.connect((host,port))
seq = 0
numPackets = 10
windowSize = 3
windowList = []
msgList = []
while True:
	data = s.recv(1024)
	print data
	response = raw_input()
	s.send(response)

