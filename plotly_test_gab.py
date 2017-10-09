import plotly as py
import plotly.graph_objs as go
import numpy as np
import os
import sys
import shutil
import time as t

py.tools.set_credentials_file(username='gabcar', api_key='a1M0F3ZTssR0IXIZyH7H')

signal = []
mean = []
bpm = []
time = []
count = 0

def update_graph(data_dict,count):
    """
        Updates graph to plotly
    """
    trace1 = go.Scatter(
        x=data_dict['time'],
        y=data_dict['signal']
    )
    trace2 = go.Scatter(
        x=data_dict['time'],
        y=data_dict['mean']
    )
    data = [trace1,trace2]
    plot_url = py.plotly.plot(data, filename='my plot')
    t.sleep(5)
    f1 = open('data_set_' + str(count) + '.txt', 'r')
    f2 = open('ecg_data_0.txt', 'w')

    data = f1.read()
    f2.write(data)
    print f2
    f1.close()
    f2.close()




prev_time = 0

if len(sys.argv)>1:
    file_path = sys.argv[1]
else:
    file_path = "ecg_data_0.txt"

while(True):
    change_time = os.stat(file_path).st_mtime #time of last change of document
    if change_time != prev_time: #check if prev time == time of last change
        prev_time = change_time
        print 1

        MESSAGES = open(file_path,"r")
        data = MESSAGES.read()
        data = data.split('\n')

        for line in data:
            split_line = line.replace('u','').replace('\'','').replace(',','').replace(')','').replace('(','')
            split_line = split_line.split(' ')
            if len(split_line)>1: #makes sure last line is skipped
                signal.append(split_line[0])
                mean.append(split_line[1])
                bpm.append(split_line[2])
                time.append(split_line[3])
                #order.append(split_line[4])

        time[:] = [float(a) for a in time]
        time[:] = [x-float(min(time)) for x in time]
        time[:] = [str(a) for a in time]

        print time[-1]

        data_dict = {'signal' : signal, 'mean' : mean, 'bpm' : bpm, 'time' : time}



        update_graph(data_dict,count)
        count +=1
