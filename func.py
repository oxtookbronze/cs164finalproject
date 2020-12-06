import socket
import sys
'''FUNCTIONS'''
def tupleToString(t):
	s=""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

def createSocket():
	
	HOST = ''	# Symbolic name meaning all available interfaces
	PORT = 9486	# Arbitrary non-privileged port

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print 'Socket created'

	'''
	Bind socket to local host and port
	'''
	try:
		s.bind((HOST, PORT))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	print 'Socket bind complete'
	return s
