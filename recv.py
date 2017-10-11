#! /usr/bin/python

import sys,time
from serial import Serial


def read_serial(s):
    i = 0
    interval = 5
    list = []
    prev_time = 0
    while True:
        if s.inWaiting() != 0
            line = s.readline()
            line = line.decode('ascii').strip("\r\n")
            time_now = time.time()
            print(line, time_now, i)
            i = i + 1
            list.append(line,time_now,i)
            if time.time - prev_time >= interval:
                f = open('ecg_data.txt','w')
                [f.write(x) for x in list]
                prev_time = time_now
                list = []
                f.close()
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
