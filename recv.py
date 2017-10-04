#! /usr/bin/python

import sys,time
from serial import Serial

    
def read_serial(s):
    i = 0
    while True:
        if s.inWaiting() != 0:
            line = s.readline()
            line = line.decode('ascii').strip("\r\n")
            print(line, time.time(), i)
            i = i + 1
        time.sleep(0.001)
    


def main(args = None):
    if args is None:
        args = sys.argv
    port,baudrate = 'COM4', 115200
    if len(args) > 1:
        port = args[1]
    if len(args) > 2:
        baudrate = int(args[2])

    s = Serial(port, baudrate)
    read_serial(s)

    return 0

if __name__ == '__main__':
    sys.exit(main())
