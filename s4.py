import time
import clientThreads
from thread import *
'''
return s
Function Definition
'''
s = clientThreads.func.createSocket()
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
# TODO: Part-1 : create a var to store username && password. NOTE: A set of username/password pairs are hardcoded here. 
clients = []
userpass = [('a','a'), ('b','b'),('c','c')]
messages = [] 
subscriptions = [ 'Project1' ]  
subscriptionUserMap = []
#PAR
count = 0 
start_new_thread(clientThreads.receiveClients ,(s,clients,count,messages,subscriptions,subscriptionUserMap,userpass))

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
