import socket
import matplotlib.pyplot as plt
import re
import numpy as np
from Canvas import Window

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

class MyServer(object):
    def __init__(self):
        self.signal = []
        self.mean= []
        self.time = []
        self.bpm = []
        self.totalPackages = 0
        
    def getConnection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        conn, addr = s.accept()
        print 'Connection address:', addr
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            print "received data:", data
            conn.send(data)  # echo
            no_of_packages +=1
            packages.append(data)
        conn.close()
        
        self.totalPackages = ''.join(packages)
    
    def splitData(self):
        splitPackages = self.totalPackages.split('\n')
        self.totalPackages = 0
        # split string
        for line in test:
            splitLine = line.replace('u','').replace('\'','').replace(',','').replace(')','').replace('(','')
            splitLine = splitLine.split(' ')
            if len(split_line)>1:
                #print split_line
                self.signal.append(splitLine[0])
                self.mean.append(splitLine[1])
                self.bpm.append(splitLine[2])
                self.time.append(splitLine[3])
                order.append(splitLine[4]) #behövs denna?
        
    def plotData(self):
        plt.ion()
        fig = plt.figure()
        window_size = 100
         
        h1 = plt.plot([],[])
        self.time[:] = [float(a) for a in time]
        self.time[:] = [x-float(min(time)) for x in time]
         
        ax = fig.add_subplot(111)
        signalLine, = ax.plot(self.time[0:window_size], self.signal[0:window_size], 'b-')
        meanLine, = ax.plot(self.time[0:window_size], self.mean[0:window_size], 'r-')
     
        for idx in range(len(time)):
            signalLine.set_data(self.time[idx:idx+window_size], self.signal[idx:idx+window_size])
            meanLine.set_data(self.time[idx:idx+window_size], self.mean[idx:idx+window_size])

            # recompute the ax.dataLim
            ax.relim()
            # update ax.viewLim using the new dataLim
            ax.set_autoscale_on(1)
            ax.set_xlim(self.time[idx],time[idx+window_size])
            plt.draw()
         
            fig.canvas.draw()
            plt.pause(0.02)
            