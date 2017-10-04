import socket
import numpy as np

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGES = open("example_pulse.txt","r")
MESSAGE = MESSAGES.read()

#control variables & list
control = 1
idx = 0
MESSAGES = []
prev_idx = 0

#divide the "messages" into buffer_size pieces
for idx in range(BUFFER_SIZE,len(MESSAGE),BUFFER_SIZE):
    MESSAGES.append(MESSAGE[prev_idx:idx])
    prev_idx = idx
MESSAGES.append(MESSAGE[prev_idx:len(MESSAGE)])


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

check = 0

for line in MESSAGES:
    s.send(line)
    check += len(line)
    data = s.recv(BUFFER_SIZE)
    print "received data:", data
print check
s.close()
