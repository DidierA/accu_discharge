
import argparse
import serial
import itertools

import csv

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from rlpro import ReloadPro

"""
Accumulator discharge graph.
based on https://matplotlib.org/gallery/animation/animate_decay.html#sphx-glr-gallery-animation-animate-decay-py
and https://github.com/arachnidlabs/rlpro-python/blob/master/rlpro/characterize.py
"""

parser = argparse.ArgumentParser(description="Evaluate capacity of an accumulator")

parser.add_argument(
	'--current',
	action='store',
	dest='test_current',
	metavar='AMPS',
	default=0.5,
	type=float,
	help="Current to test with")
parser.add_argument(
	'--delay',
	action='store',
	dest='delay',
	metavar='SECONDS',
	default=60.0,
	type=float,
	help="Interval between measurements")
parser.add_argument(
	'--baudrate',
	action='store',
	dest='baudrate',
	metavar='BAUD',
	default=115200,
	type=int,
	help="Baud rate to use when flashing using serial (default 115200)")
parser.add_argument(
	'--timeout',
	action='store',
	dest='timeout',
	metavar='SECS',
	default=5.0,
	type=float,
	help="Time to wait for a Bootloader response (default 5)")
parser.add_argument(
	'--min_voltage',
	action='store',
	dest='min_volt',
	metavar='VOLTS',
	default=1,
	type=float,
	help="Minimum voltage to reach")
parser.add_argument(
	'port',
	action='store',
	metavar='PORT',
	default=None,
	help="Serial port to use")
parser.add_argument(
	'--file',
	type=argparse.FileType('w'),
	help="CSV file to create")

def output(args,string):
	print string
	if (args.file):
		args.file.write("%s\n" % string)

# generator called at each frame to get new data
# autonomous sinus generator
# def data_gen():
#     for cnt in itertools.count():
#         t = cnt / 10
#         # print("data_gen")
#         if (t<=100): 
#             y1=np.sin(2*np.pi*t/5)
#             y2=np.sin(2*np.pi*t/3)
#             yield t, y1, y2
#         else:
#             ani._stop() # stops the animation, private undocumented function


#
# read data from file
# def data_gen():
#         with open('cell_18650.csv') as f:
#             csv_reader=csv.reader(f, delimiter=';')
#             for row in csv_reader:
#                 if len(row) != 4:
#                     continue
#                 (sec,amp,volts,mAh) = row[0:4]
#                 print (sec,amp,volts,mAh)
#                 try:
#                     yield int(sec), [float(amp), float(volts)]
#                 except ValueError:
#                     print('Invalid line %s'%';'.join(row))

# use reload pro
def data_gen():
    global first,volt, seconds, capacity, rl, previous_amp
    while (first) or (volt > args.min_volt):
        rl.set(args.test_current)
        if first: 
            # wait for current to settle
            previous_time=time.time()
            previous_amp=0
            time.sleep(1)
            first=False

        amp, volt = rl.read()
        current_time=time.time()

        if (volt <= args.min_volt):
            rl.set(0.0)
            output(args, "end. Measured capatity: %d mAh in %d seconds" % (capacity / 3.6, seconds))
        else:
            time_step=current_time - previous_time
            capacity += (amp+previous_amp)*time_step/2.0
            seconds += time_step
            
            output(args, "%.2f;%.2f;%.2f;%d" % (seconds, amp, volt, capacity / 3.6))
            previous_amp=amp
            previous_time=current_time
            yield(seconds, [amp, volt])

# called once. sets up graphics and data objs
def init():
    for a in ax:
        a.set_ylim(0, .1)
        a.set_xlim(0, 10)

    ax[0].set_ylabel("Curent (A)")
    
    # ax[1].set_xlablel("time")
    ax[1].set_ylabel("Voltage (V)")
    ax[1].set_ylim(args.min_volt,args.min_volt+.1)

    del xdata[:]
    del y1data[:]
    del y2data[:]
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    return [line1,line2]

# called at each frame with the result of data_gen
def run(data):
    # update the data
    y= []
    t, y = data

    (y1, y2) = y
    # print ('%f %f %f' % (t, y1, y2))

    xdata.append(t)
    y1data.append(y1)
    y2data.append(y2)

    # autoscale x
    xmin, xmax = ax[0].get_xlim()
    if t >= xmax:
        for a in ax:
            a.set_xlim(xmin, t+(t-xmin)/10)
            a.figure.canvas.draw()
    
    # autoscale y
    # If value is out of bonds, extend the scale by 10%.
    for i in range(2):
        ymin, ymax = ax[i].get_ylim()

        if y[i] >= ymax:
            ymax=y[i]+(y[i]-ymin)/10
            ax[i].set_ylim(ymin, ymax)
            ax[i].figure.canvas.draw()
            
        if y[i] <= ymin:
            ymin=y[i]-(ymax-y[i])/10
            ax[i].set_ylim(ymin, ymax)
            ax[i].figure.canvas.draw()

    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)

    return [line1,line2]

args = parser.parse_args()
s = serial.Serial(args.port, args.baudrate, timeout=args.timeout)
rl = ReloadPro(s)

# Set up graphic grid
fig, ax = plt.subplots(2,1, sharex=True)

# Remove horizontal space between axes
fig.subplots_adjust(hspace=0)

line1, = ax[0].plot([], [], lw=2)
line2, = ax[1].plot([], [], lw=2)
ax[0].grid(), ax[1].grid()
xdata, y1data, y2data = [], [], []

seconds=0
capacity=0

output(args, "sec;amp;volts;mAh")
first=True

ani = animation.FuncAnimation(fig, run, data_gen, interval=args.delay*1000, init_func=init, repeat=False) 
# run() will be called with data() results each interval ms

plt.show()
