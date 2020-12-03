import socket
import time
import sys
from thread import *
import getpass
import os

'''
Function Definition
'''
global serverResponse
def receiveThread(s):
	while True:
		try:
			serverResponse = s.recv(4096) # receive msg from server
			print serverResponse
			# You can add operations below once you receive msg
			# from the server

		except:
			print "Connection closed"
			break
	

def tupleToString(t):
	s = ""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
try:
	# create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();
print 'Socket Created'

'''
Resolve Hostname
'''
host = '10.0.0.4'
host = '127.0.0.1'
port = 9486
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()
print 'Ip address of ' + host + ' is ' + remote_ip

'''
Connect to remote server
'''
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

'''
TODO: Part-1.1, 1.2: 
Enter Username and Passwd
'''
# Whenever a user connects to the server, they should be asked for their username and password.
# Username should be entered as clear text but passwords should not (should be either obscured or hidden). 
# get username from input. HINT: raw_input(); get passwd from input. HINT: getpass()

# Send username && passwd to server
welcome_msg = s.recv(1024)
print welcome_msg
username = raw_input("Username:")
password = getpass.getpass(prompt = "Password:",stream = None)

s.send(tupleToString((username,password)))

'''
TODO: Part-1.3: User should log in successfully if username and password are entered correctly. A set of username/password pairs are hardcoded on the server side. 
'''
reply = s.recv(5)
if reply == 'valid': # TODO: use the correct string to replace xxx here!

	# Start the receiving thread
	start_new_thread(receiveThread ,(s,))

	message = ""
	while True :

		# TODO: Part-1.4: User should be provided with a menu. Complete the missing options in the menu!
		message = raw_input("Choose an option (type the number): \n 1.Logout \n 2.Send Broadcast Message\n 3.Change your Password\n 4.Send a Private Message\n 5.Read Unread Messages\n 6.List all the available groups\n 7.Join Group\n 8.Send Group Message\n 9.Quit Group\n")
		s.send(message)	
		try :
			# TODO: Send the selected option to the server
			# HINT: use sendto()/sendall()
			if message == str(1):
				s.send( 'Logout')
				# TODO: add logout operation
				break
			if message == str(2):
				print 'Post a message'
				message = raw_input("What would you like to post?")
				message = "From " + username + " : " + message
				s.send(message)
				time.sleep(1)
			# Add other operations, e.g. change password
			if message == str(3):
				print 'Change Password:'
				oldpass = getpass.getpass(prompt = "Old Password:",stream = None)
				newpass = getpass.getpass(prompt = "New Password:",stream = None)
				passwordCheck = (oldpass,newpass)
				s.send(tupleToString(passwordCheck))	
				time.sleep(1)
			if message == str(4):
				'''Test cases to think about: user is online, user is offline, multiple messagesonce user comes online'''
				print 'Send a Private Message'
				recvusername = raw_input("Username:")
				msg = raw_input("Message:")
				s.send(tupleToString((username,recvusername,msg)))
				time.sleep(1)	
			if message == str(5):
				time.sleep(1)
				continueMessage = getpass.getpass(prompt = "Press any key to close messages", stream = None)
			if message == str(6):
				# List all available group chats
				time.sleep(1)
				continueMessage = getpass.getpass(prompt = "Press any key to close messages", stream = None)
			if message == str(7):
				# Request to join a group chat
				print '5'	
			if message == str(8):
				# send group message
				time.sleep(1)
				groupNumber = raw_input("Group?")
				grpMsg = raw_input("Message?")
				s.send(tupleToString((groupNumber,grpMsg)))
			if message == str(9):
				print '3'
				# quit group chat
			
		except socket.error:
			print 'Send failed'
			sys.exit()
else:
	print 'Invalid username or passwword'
s.close()
