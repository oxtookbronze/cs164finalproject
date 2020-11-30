import socket
import sys
import time
from check import ip_checksum
import random

HOST = ''
PORT = 4013

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

clientsocket,address = s.accept()	

s.bind((HOST,PORT))
windowSize = 3

print "Created Socket and bind"

expecting=0
while 1:
	s.accept()
	d = s.recvfrom(1024)
	data=d[0]
	addr=d[1]
	seq=data[0]
	msg=data[1:12]
	checksum=data[12:]
	checksum2=ip_checksum(msg)
	if int(seq) != expecting:
		print 'Dropped: ', seq, '-', msg, ' ,checkusm = ', checksum,' from ',addr
		print expecting
	else:
		print seq, '-', msg, ' ,checkusm = ', checksum,' from ',addr
		expecting = (expecting +1) % windowSize
		
	if not d:
		break

	

s.close()
