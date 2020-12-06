import func
from thread import *
import options
'''
Function for handling connections. This will be used to create threads
'''
def clientThread(conn,clients,count,messages,subscriptions,subscriptionUserMap,userpass):
	# Tips: Sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	rcv_msg = conn.recv(1024)
	rcv_msg = tuple(func.stringToTuple(rcv_msg)) 
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
				options.option2(conn,clients)
			elif option == str(3):
				options.option3(conn,userpass,user)
			elif option == str(4):
				options.option4(conn,messages)
			elif option == str(5):
				options.option5(conn,messages,userpass,user)
			elif option == str(6):
				options.option6(conn,subscriptions)
			elif option == str(7):
				options.option7(conn,subscriptions,userpass,user)
			elif option == str(8):
				options.option8(conn,messages,subscriptions,userpass,user)
			elif option == str(9):
				options.option9(conn,subscriptions,subscriptionUserMap,userpass,user)		
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

def receiveClients(s,clients,count,messages,subscriptions,subscriptionUserMap,userpass):
	while 1:
		# Tips: Wait to accept a new connection (client) - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		clients.append(conn)
		# Tips: start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientThread ,(conn,clients,count,messages,subscriptions,subscriptionUserMap,userpass))


