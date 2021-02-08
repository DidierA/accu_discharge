
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
        if (t<=7.6): # stop drawing after 7.5.  Doe snot sto the animation from runing
            y1=np.sin(2*np.pi*t/5)
            y2=np.sin(2*np.pi*t/3)
            yield t, y1, y2 # * np.exp(-t/10.)
        else:
            ani._stop() # stops the animation, private undocumented function
            # yield -1, 0, 0 # without this and the test in data, the window is frozen after 7.5

# called once. sets up graphics and data objs
def init():
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(0, 8)
    del xdata[:]
    del y1data[:]
    del y2data[:]
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    return [line1,line2]

fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2)
ax.grid()
xdata, y1data, y2data = [], [], []

# called at each frame with the result of data_gen
def run(data):
    # update the data
    t, y1, y2 = data
    # print ('%f %f %f' % (t, y1, y2))
    if t==-1:
        # print ('end')
        return 
    xdata.append(t)
    y1data.append(y1)
    y2data.append(y2)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, xmax+2)
        ax.figure.canvas.draw()
    
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)

    return [line1,line2]

ani = animation.FuncAnimation(fig, run, data_gen, interval=100, init_func=init) 
# run() will be called with data() results each interval ms

plt.show()

# autoscale ?