
import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""
Accumulator discharge graph.
based on https://matplotlib.org/gallery/animation/animate_decay.html#sphx-glr-gallery-animation-animate-decay-py
"""


# generator called at each frame to get new data
def data_gen():
    for cnt in itertools.count():
        t = cnt / 10
        # print("data_gen")
        if (t<=100): 
            y1=np.sin(2*np.pi*t/5)
            y2=np.sin(2*np.pi*t/3)
            yield t, y1, y2
        else:
            ani._stop() # stops the animation, private undocumented function

# called once. sets up graphics and data objs
def init():
    for a in ax:
        a.set_ylim(-1.1, 1.1)
        a.set_xlim(0, 8)

    
    ax[0].set_ylabel("Curent (A)")
    
    # ax[1].set_xlablel("time")
    ax[1].set_ylabel("Voltage (V)")

    del xdata[:]
    del y1data[:]
    del y2data[:]
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    return [line1,line2]

fig, ax = plt.subplots(2,1, sharex=True)

# Remove horizontal space between axes
fig.subplots_adjust(hspace=0)

line1, = ax[0].plot([], [], lw=2)
line2, = ax[1].plot([], [], lw=2)
ax[0].grid(), ax[1].grid()
xdata, y1data, y2data = [], [], []

# called at each frame with the result of data_gen
def run(data):
    # update the data
    t, y1, y2 = data
    # print ('%f %f %f' % (t, y1, y2))

    xdata.append(t)
    y1data.append(y1)
    y2data.append(y2)
    xmin, xmax = ax[0].get_xlim()

    if t >= xmax:
        for a in ax:
            a.set_xlim(xmin, xmax+(xmax-xmin)/10)
            a.figure.canvas.draw()
    
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)

    return [line1,line2]

ani = animation.FuncAnimation(fig, run, data_gen, interval=100, init_func=init) 
# run() will be called with data() results each interval ms

plt.show()

# autoscale ?