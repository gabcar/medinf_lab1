#! /usr/bin/python

import sys,time
import Tkinter as tk
from serial import Serial

class App(tk.Frame):
    i = 0
    def __init__(self, parent, title, serialPort):
        tk.Frame.__init__(self, parent)
        self.serialPort = serialPort
        self.npoints = 100
        self.Y1 = [0 for x in range(self.npoints)]
        self.Y2 = [0 for x in range(self.npoints)]
        self.bpm = 0
        parent.wm_title(title)
        parent.wm_geometry("800x400")
        self.canvas = tk.Canvas(self, background="white")
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.create_line((0, 0, 0, 0), tag='Y1', fill='darkred', width=1)
        self.canvas.create_line((0, 0, 0, 0), tag='Y2', fill='darkblue', width=1)
        self.canvas.create_text((10, 390), tag='bpm', anchor='sw', text="- bpm")
        self.canvas.grid(sticky="news")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky="news")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
    
    def on_resize(self, event):
        self.replot()
    
    def read_serial(self):
        """
            Check for input from the serial port. On fetching a line, parse
            the sensor values and append to the stored data and post a replot
            request.
            """
        if self.serialPort.inWaiting() != 0:
            line = self.serialPort.readline()
            line = line.decode('ascii').strip("\r\n")
            print(line, time.time(), App.i) # line not a valid sensor result.
            App.i = App.i + 1
            try:
                newY1,newY2,bpm = line.strip().split(" ")
                newY1 = int(newY1)
                newY2 = int(newY2)
                self.bpm = int(bpm)
                self.Y1.append(newY1)
                self.Y2.append(newY2)
                self.Y1 = self.Y1[-1 * self.npoints:]
                self.Y2 = self.Y2[-1 * self.npoints:]
            except Exception as e:
                print(e)
            self.replot()
        self.after(5, self.read_serial)
    
    
    def replot(self):
        """
            Update the canvas graph lines from the cached data lists.
            The lines are scaled to match the canvas size as the window may
            be resized by the user.
            """
        w = self.winfo_width()
        h = self.winfo_height()
        max_Y = 1024.0
        coordsY1 = []
        coordsY2 = []
        for n in range(0, self.npoints):
            x = (w * n) / self.npoints
            coordsY1.append(x)
            coordsY1.append(int(h - ((h * (self.Y1[n]+100)) / max_Y)))
            coordsY2.append(x)
            coordsY2.append(int(h - ((h * (self.Y2[n]+100)) / max_Y)))
        #print "replot", coordsY
        self.canvas.coords('Y1', *coordsY1)
        self.canvas.coords('Y2', *coordsY2)
        bpmtext = "%d bpm" % self.bpm
        self.canvas.itemconfig('bpm', text=bpmtext)

def main(args = None):
    if args is None:
        args = sys.argv
    port,baudrate = 'COM4', 115200
    if len(args) > 1:
        port = args[1]
    if len(args) > 2:
        baudrate = int(args[2])
    root = tk.Tk()
    app = App(root, "Smooth Sailing", Serial(port, baudrate))
    app.read_serial()
    app.mainloop()
    return 0

if __name__ == '__main__':
    sys.exit(main())
