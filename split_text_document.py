import os
import sys
import numpy as np
import time

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

file_path = "example_pulse.txt"
f = open(file_path,"r")
data = f.read()
data = data.split('\n')

idxs = []
time = []

for line in data:
    split_line = line.replace('u','').replace('\'','').replace(',','').replace(')','').replace('(','')
    split_line = split_line.split(' ')
    if len(split_line)>1: #makes sure last line is skipped
        time.append(split_line[3])
        #order.append(split_line[4])
time[:] = [float(a) for a in time]
time[:] = [x-float(min(time)) for x in time]


temp =0
for i,times in enumerate(time):
    if times - temp > 5:
        idxs.append(i)
        temp = times

print idxs
for i in idxs:
    print time[i]

temp = 0
for num,i in enumerate(idxs):
    f = open("data_set_" + str(num) + ".txt","w")
    for line in data[temp:i]:
        f.write(str(line) + '\n')
    temp = i
    f.close()
