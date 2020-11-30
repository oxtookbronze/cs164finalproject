
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
port =40213

seq = 0
numPackets = 10
windowSize = 3
windowList = []
msgList = []
s.setblocking(0)
s.settimeout(1)

s.sendto("hello world!",(host,port))

