import socket
import matplotlib.pyplot as plt
import re
import numpy as np

class tcp_server(object):
    def __init__(self):
        self.signal = []
        self.mean = []
        self.bpm = []
        self.time = []
        self.raw = []

    def getConnection(self):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
        no_of_packages =0
        packages = []

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
            print 'get connection'
        conn.close()
        total_packages = ''.join(packages)
        self.raw = total_packages

    def splitData(self):
        test = self.raw.split('\n')

        # split string
        for line in test:
            split_line = line.replace('u','').replace('\'','').replace(',','').replace(')','').replace('(','')
            split_line = split_line.split(' ')
            if len(split_line)>1: #makes sure last line is skipped
                self.signal.append(split_line[0])
                self.mean.append(split_line[1])
                self.bpm.append(split_line[2])
                self.time.append(split_line[3])
                #order.append(split_line[4])
        self.time[:] = [float(a) for a in self.time]
        self.time[:] = [x-float(min(self.time)) for x in self.time]

    def plotData(self):
        plt.ion() #interactive on
        fig = plt.figure()
        window_size = 100

        h1 = plt.plot([],[])
         #convert to float

        ax = fig.add_subplot(111)
        signal_window= np.array(self.signal[0:window_size])
        time_window = np.array(self.time[0:window_size])
        mean_window = np.array(self.mean[0:window_size])

        line1, = ax.plot(time_window, signal_window, 'b-')
        line2, = ax.plot(time_window, mean_window, 'r-')

        for idx in range(len(self.time)):
            line1.set_ydata(self.signal[idx:idx+window_size])
            line2.set_ydata(self.mean[idx:idx+window_size])
            line1.set_xdata(self.time[idx:idx+window_size])
            line2.set_xdata(self.time[idx:idx+window_size])

            # recompute the ax.dataLim
            ax.relim()
            # update ax.viewLim using the new dataLim
            ax.set_autoscaley_on(1)
            ax.set_xlim(self.time[idx],self.time[idx+window_size])
            plt.draw()

            fig.canvas.draw()
            plt.pause(0.02)

if __name__ == '__main__':
    s = tcp_server()
    s.getConnection()
    s.splitData()
    s.plotData()
