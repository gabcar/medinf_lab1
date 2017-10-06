import plotly as py
import plotly.graph_objs as go
import numpy as np
import os
import sys

py.tools.set_credentials_file(username='gabcar', api_key='a1M0F3ZTssR0IXIZyH7H')

def update_graph(data_dict):
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

signal = []
mean = []
bpm = []
time = []

prev_time = 0

if len(sys.argv)>1:
    file_path = sys.argv[1]
else:
    file_path = "example_pulse.txt"

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

        data_dict = {'signal' : signal, 'mean' : mean, 'bpm' : bpm, 'time' : time}

        update_graph(data_dict)
