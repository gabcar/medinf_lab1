import sys
import logging
import time
import socket
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        connectToServer()
        sendData()

def connectToServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    return s

def sendData(s):
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
    check = 0
    for line in MESSAGES:
        s.send(line)
        check += len(line)
        
        data = s.recv(BUFFER_SIZE)
        print "received data:", data
    s.close()

if __name__ == "__main__":
    s = connectToServer()
    sendData(s)
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
