import socket
import sys
import hashlib
from curses.ascii import ctrl
from thread import *
import telnetlib

HOST = ''	# Symbolic name meaning all available interfaces
PORT = 9999# Arbitrary non-privileged port



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def hsh(string):
	return str(hashlib.sha256(str.encode(string)).hexdigest())		


userListFile= open("userListFile.txt","a+")
# Abstraction for Dialog
try:
	userList = eval(userListFile.read()) 
except Exception as err:
	print err
	userList = { 'a' : hsh('a')}
userListFile.close()
print userList

def prompt(conn,msg):
	conn.send(msg)
	response = conn.recv(1024)
	return response[:-2]

class Client:
	def __init__(self,conn):
		self.conn = conn
	usr = ""
	pas = ""
	def tick(self):


		if self.usr == "":
			msg = "Welcome to the server. Please enter your username:"
			usr = prompt(conn,msg)
			
		if self.pas == "":
					
			conn.send(ctrl(']'))
		if usr in userList:
			if hsh(pas) == userList[usr]:
				conn.send("Login Successful")
			else:
				conn.send("Incorrect Credentials\n")
		else:
			pas = prompt(conn, "I see you are new here. What would you like your password to be.\n")
			userList[usr] = hsh(pas)
			userListFile = open("userListFile.txt","w")
			userListFile.write(str(userList))
	
print 'Socket created'

#Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
	
print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	x = Client(conn)	
	#infinite loop so that function do not terminate and thread do not end.
	x.tick()
	#came out of loop
	conn.close()
while True:
#now keep talking with the client
    #wait to accept a connection - blocking call
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	
	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
	start_new_thread(clientthread ,(conn,))

s.close()
