import socket
import matplotlib.pyplot as plt
import re
import numpy as np

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
conn.close()

total_packages = ''.join(packages)
print len(total_packages)
print no_of_packages

test = total_packages.split('\n')

signal = []
mean = []
bpm = []
time = []
order = []

# split string
for line in test:
    split_line = line.replace('u','').replace('\'','').replace(',','').replace(')','').replace('(','')
    split_line = split_line.split(' ')
    if len(split_line)>1:
        #print split_line
        signal.append(split_line[0])
        mean.append(split_line[1])
        bpm.append(split_line[2])
        time.append(split_line[3])
        order.append(split_line[4])

#plot stuff
plt.ion()
fig = plt.figure()
window_size = 100

h1 = plt.plot([],[])
time[:] = [float(a) for a in time]
time[:] = [x-float(min(time)) for x in time]

ax = fig.add_subplot(111)
signal_window= np.array(signal[0:window_size])
time_window = np.array(time[0:window_size])
mean_window = np.array(mean[0:window_size])

line1, = ax.plot(time_window, signal_window, 'b-')
line2, = ax.plot(time_window, mean_window, 'r-')

for idx in range(len(time)):
    line1.set_ydata(signal[idx:idx+window_size])
    line2.set_ydata(mean[idx:idx+window_size])
    line1.set_xdata(time[idx:idx+window_size])
    line2.set_xdata(time[idx:idx+window_size])

    plt.title('bpm: ' + bpm[idx])

    #ax1 = plt.gca()
    # recompute the ax.dataLim
    ax.relim()
    # update ax.viewLim using the new dataLim
    ax.set_autoscale_on(1)
    ax.set_xlim(time[idx],time[idx+window_size])
    plt.draw()

    fig.canvas.draw()
    plt.pause(0.02)
