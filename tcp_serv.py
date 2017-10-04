import socket
import matplotlib.pyplot as plt
import re

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


for line in test:
    split_line = line.replace('u','').replace('\'','').replace(',','').replace(')','').replace('(','')
    split_line = split_line.split(' ')
    if len(split_line)>1:
        print split_line
        signal.append(split_line[0])
        mean.append(split_line[1])
        bpm.append(split_line[2])
        time.append(split_line[3])
        order.append(split_line[4])

end_of_time=len(time)
plt.figure()

plt.plot(time[end_of_time-200:end_of_time-1],signal[end_of_time-200:end_of_time-1])
plt.plot(time[end_of_time-200:end_of_time-1],mean[end_of_time-200:end_of_time-1])
plt.title(bpm[end_of_time-1])
plt.show()



#print test
print len(test)
print test[0]
