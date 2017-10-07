import plotly
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import sys
import os
import time

tls.set_credentials_file(username='nieag', api_key='5QfINFhFRDHva9LFur0Z', stream_ids=['n5itayip3i', 'm1gou1qqm4'])
stream_ids = tls.get_credentials_file()['stream_ids']
print stream_ids

class onlineEcg(object):
    
    def __init__(self):
        self.signal = []
        self.mean = []
        self.bpm = []
        self.ecgTime = []
        
    def appendData(self):
        prev_time = 0
        
        if len(sys.argv)>1:
            file_path = sys.argv[1]
        else:
            file_path = "short_pulse.txt"
        
        
        MESSAGES = open(file_path,"r")
        data = MESSAGES.read()
        data = data.split('\n')
        
        
        for line in data:
            split_line = line.replace('u','').replace('\'','').replace(',','').replace(')','').replace('(','')
            split_line = split_line.split(' ')
            if len(split_line)>1: #makes sure last line is skipped
                self.signal.append(split_line[0])
                self.mean.append(split_line[1])
                self.bpm.append(split_line[2])
                self.ecgTime.append(split_line[3])
                #order.append(split_line[4])
        self.ecgTime[:] = [float(a) for a in self.ecgTime]
        self.ecgTime[:] = [x-float(min(self.ecgTime)) for x in self.ecgTime]
        self.ecgTime[:] = [str(a) for a in self.ecgTime]
        
        data_dict = {'self.signal' : self.signal, 'self.mean' : self.mean, 'bpm' : self.bpm, 'time' : self.ecgTime}
    
    def ecgStream(self):
        stream_1 = dict(token=stream_ids[0], maxpoints=80)
        stream_2 = dict(token=stream_ids[1], maxpoints=80)
        
        
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
        time.sleep(5)
        i = 0
        print len(self.signal)
        while True:
            if len(self.signal) < 10:
                self.appendData()
            # Send data to your plot
            s1.write(dict(x=i, y=self.signal[0]))
            s2.write(dict(x=i, y=self.mean[0]))
            del self.signal[0], self.mean[0]
            print i
            print len(self.ecgTime), len(self.signal), len(self.mean)
            i += 1
            time.sleep(0.5)  # plot a point every second    
        # Close the stream when done plotting
        s.close()
        
if __name__ == "__main__":
    test = onlineEcg()
    test.appendData()
    test.ecgStream()
