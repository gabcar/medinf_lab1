import plotly
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import sys
import os
import time as t

#y.tools.set_credentials_file(username='gabcar', api_key='a1M0F3ZTssR0IXIZyH7H')

signal = []
mean = []
bpm = []
time = []

def ecgStream():
    tls.set_credentials_file(username='gabcar', api_key='a1M0F3ZTssR0IXIZyH7H', stream_ids=['oigavorxjl', 'i4ux8rumfc'])
    stream_ids = tls.get_credentials_file()['stream_ids']

    stream_1 = dict(token=stream_ids[0], maxpoints=300)
    stream_2 = dict(token=stream_ids[1], maxpoints=300)

    # Initialize trace of streaming plot by embedding the unique stream_id
    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='lines',
        stream=stream_1         # (!) embed stream id, 1 per trace
    )
    trace2 = go.Scatter(
        x=[],
        y=[],
        mode='lines',
        stream=stream_2
    )

    plotData = [trace1, trace2]

    # Add title to layout object
    layout = go.Layout(title='Pulse curve')

    # Make a figure object
    fig = go.Figure(data=plotData, layout=layout)

    # Send fig to Plotly, initialize streaming plot, open new tab
    py.plot(fig, filename='python-streaming')

    # We will provide the stream link object the same token that's associated with the trace we wish to stream to
    s1 = py.Stream(stream_ids[0])
    s2 = py.Stream(stream_ids[1])
    # We then open a connection
    s1.open()
    s2.open()
    # Delay start of stream by 5 sec (time to switch tabs)
    t.sleep(5)
    i = 0
    prev_time = 0
    count = 1
    time_offset = False
    #print len(self.signal)
    while True:

        change_time = os.stat(file_path).st_mtime #time of last change of document
        if change_time != prev_time: #check if prev time == time of last change
            prev_time = change_time
            t.sleep(0.5)
            MESSAGES = open(file_path,"r")
            data = MESSAGES.read()
            MESSAGES.close()
            data = data.split('\n')
            print 'file changed'



            signal =[]
            mean = []
            bpm = []
            time = []

            for line in data:
                split_line = line.replace('u','').replace('\'','').replace(',','').replace(')','').replace('(','')
                split_line = split_line.split(' ')
                if len(split_line)>1: #makes sure last line is skipped
                    signal.append(split_line[0])
                    mean.append(split_line[1])
                    bpm.append(split_line[2])
                    time.append(split_line[3])
                    #order.append(split_line[4])
            if time_offset == False:
                time_offset = float(time[0])

            time[:] = [float(a) for a in time]
            time[:] = [x-time_offset for x in time]
            time[:] = [str(a) for a in time]
            print time[0:5]
            print data[0:5]
            s1.write(dict(x=time, y=signal))
            s2.write(dict(x=time, y=mean))
    #s.close()


if len(sys.argv)>1:
    file_path = sys.argv[1]
else:
    file_path = "ecg_data.txt"

ecgStream()
