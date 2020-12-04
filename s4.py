import socket
import sys
from thread import *
import time

'''
Function Definition
'''
def tupleToString(t):
	s=""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
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

'''
Start listening on socket
'''
s.listen(10)
print 'Socket now listening'

'''
Define variables:
username && passwd
message queue for each user
'''
clients = []
# TODO: Part-1 : create a var to store username && password. NOTE: A set of username/password pairs are hardcoded here. 
userpass = [('a','a'), ('b','b'),('c','c')]
messages = [] 
subscriptions = [ 'Project1' ]  
subscriptionUserMap = []
count = 0
#PAR

'''
Function for handling connections. This will be used to create threads
'''
def clientThread(conn):
	global clients
	global count
	# Tips: Sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	rcv_msg = conn.recv(1024)
	rcv_msg = tuple(stringToTuple(rcv_msg)) 
	if rcv_msg in userpass:
		
		user = userpass.index(rcv_msg)
			
		try :
			conn.sendall('valid')
		except socket.error as err:
			print 'Send failed', err
			sys.exit()
			
		# Tips: Infinite loop so that function do not terminate and thread do not end.
		while True:
			try:	
				option = conn.recv(1024)
			except:
				break
			
			if option == str(1):
				print 'user logout'
				break
				# TODO: Part-1: Add the logout processing here	
				conn.recv(1024)
			elif option == str(2):
				print 'Post a message'
				message = conn.recv(1024)
				for conn in clients:
					conn.send(message)
				conn.send("\nMessage Sent")
			elif option == str(3):
				print 'Change Password'
				passwordTuple = conn.recv(1024)
				passwordTuple = tuple(stringToTuple(passwordTuple))
				if userpass[user][1] == passwordTuple[0]:
					conn.send("Password Changed")
					userpass.append((userpass[user][0],passwordTuple[1]))
					del userpass[user]
				else:
					conn.send("Password Incorrect") 
			elif option == str(4):
				messageTuple = conn.recv(1024)
				messageTuple = tuple(stringToTuple(messageTuple))
				messages.append(messageTuple)
			elif option == str(5):
				for i in range(0,len(messages)):
					if messages[i][1] == userpass[user][0]:
						tmp =  str(messages[0] + ' says ' + messages[i][2])
						conn.send(tmp)
						del messages[i]
						i-=1
			elif option == str(6):
				for gc in subscriptions:
					msg = gc + '\n'
					conn.send(msg)				
			elif option == str(7):
				for gc in range(len(subscriptions)):
					msg = str(gc) +  ' ' + subscriptions[gc] + '\n'
					conn.send(msg)				
				conn.send("Enter the # of the group")
				opt = conn.recv(1024)
				try:
					if (userpass[user][0], subscriptions[int(opt)]) not in subscriptionUserMap:

						subscriptionUserMap.append( (userpass[user][0], subscriptions[int(opt)]) )
					
				except:
					conn.send("invalid option chosen")
			elif option == str(8):
				for i in range(0,len(subscriptions)):
					for j in subscriptionUserMap:	
						if j[0] == userpass[user][0]:
							msg = str(i) +' ' +  j[1] + '\n'
							conn.send(msg)
				gcMsg = conn.recv(1024)
				gcMsg = tuple(stringToTuple(gcMsg))
				print gcMsg
				for i in subscriptionUserMap:
					print 'i', i
					print 'userMap',subscriptionUserMap[int(gcMsg[0])] 
					if i[1] == subscriptions[int(gcMsg[0])]: 
						messages.append( (i[1], i[0], gcMsg[1]))
				print 'messages:'
				print messages
			elif option == str(9):
				for i in range(0,len(subscriptions)):
					for j in subscriptionUserMap:	
						if j[0] == userpass[user][0]:
							msg = str(i) +' ' +  j[1] + '\n'
							conn.send(msg)
				conn.send("Group #?")
				groupNum = conn.recv(1024)
				subscriptionUserMap.remove( (userpass[user][0] , subscriptions[int(groupNum)])) 

				

						
			else:
				try :
					conn.sendall('Option not valid')
				except socket.error as err:
					print err
					print 'option not valid Send failed'
					conn.close()
					clients.remove(conn)
	else:
		try :
			conn.sendall('Invalid')
		except socket.error:
			print 'Invalid Send failed'
	print 'Logged out'
	conn.close()
	if conn in clients:
		clients.remove(conn)

def receiveClients(s):
	global clients
	while 1:
		# Tips: Wait to accept a new connection (client) - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		clients.append(conn)
		# Tips: start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientThread ,(conn,))

start_new_thread(receiveClients ,(s,))

'''
main thread of the server
print out the stats
'''
while 1:
	message = raw_input()	
	if message == 'messagecount':
		print 'Since the server was opened ' + str(count) + ' messages have been sent'
	elif message == 'usercount':
		print 'There are ' + str(len(clients)) + ' current users connected'
	elif message == 'storedcount':
		print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'
	elif message == 'newuser':
		user = raw_input('User:\n')
		password = raw_input('Password:')
		userpass.append([user, password])
		messages.append([])
		subscriptions.append([])
		print 'User created'
		 
			
s.close()
