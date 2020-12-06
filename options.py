import func
def option2(conn,clients):
	print 'Post a message'
	message = conn.recv(1024)
	for conn in clients:
		conn.send(message)
def option3(conn,userpass,user):
	print 'Change Password'
	passwordTuple = conn.recv(1024)
	passwordTuple = tuple(func.stringToTuple(passwordTuple))
	if userpass[user][1] == passwordTuple[0]:
		conn.send("Password Changed")
		userpass.append((userpass[user][0],passwordTuple[1]))
		del userpass[user]
	else:
		conn.send("Password Incorrect") 
def option4(conn,messages):
	messageTuple = conn.recv(1024)
	messageTuple = tuple(func.stringToTuple(messageTuple))
	messages.append(messageTuple)
	print messages
def option5(conn,messages,userpass,user):
	print len(messages)
	for i in range(len(messages)):
		print i, messages[i]
		if messages[i][1] == userpass[user][0]:
			tmp =  str(messages[i][0] + ' says ' + messages[i][2] + '\n')
			conn.send(tmp)

def option6(conn,subscriptions):
	for gc in subscriptions:
		msg = gc + '\n'
		conn.send(msg)				
def option7(conn,subscriptions,userpass,user):
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
def option8(conn,subscriptions,userpass,user):
	for i in range(0,len(subscriptions)):
		for j in subscriptionUserMap:	
			if j[0] == userpass[user][0]:
				msg = str(i) +' ' +  j[1] + '\n'
				conn.send(msg)
	gcMsg = conn.recv(1024)
	gcMsg = tuple(func.stringToTuple(gcMsg))
	print gcMsg
	for i in subscriptionUserMap:
		print 'i', i
		print 'userMap',subscriptionUserMap[int(gcMsg[0])] 
		if i[1] == subscriptions[int(gcMsg[0])]: 
			messages.append( (i[1], i[0], gcMsg[1]))
	print 'messages:'
	print messages
def option9():
	try:
		for i in range(0,len(subscriptions)):
			for j in subscriptionUserMap:	
				if j[0] == userpass[user][0]:
					msg = str(i) +' ' +  j[1] + '\n'
					conn.send(msg)
		conn.send("Group #?")
		groupNum = conn.recv(1024)
		subscriptionUserMap.remove( (userpass[user][0] , subscriptions[int(groupNum)])) 

	except:
		pass
	
