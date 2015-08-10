#!/usr/bin/python

import argparse
import re
import pylab
import subprocess
from time import sleep
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation


def main():
    harry_plotter()


def reg_that_shit(string):
    string = string
    grep = re.search(r'time=\d\d\.\d', string)
    if grep is None:
        return 0
    else:
        grep = grep.group(0)
        grep1 = re.search(r'\d\d\.\d', grep)
        match = grep1.group(0)
        return match


def args_smargs():
    the_parser = argparse.ArgumentParser(description='My crazy program for fun')
    the_parser.add_argument('host', help='Host-name or IP address')
    the_parser.add_argument('count', help='Ping repeat count')
    the_args = the_parser.parse_args()
    the_return = the_args.host, the_args.count
    return the_return


def ping_thing():
    cmd_ping = 'ping %s -c %s' % args_smargs()
    ping_probe = subprocess.Popen(cmd_ping, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)

    while True:
        line = ping_probe.stdout.readline()
        ping_probe.stdout.flush()
        output = reg_that_shit(line)
        return int(output)
        sleep(3)
        if line == '' and ping_probe.poll() != None:
            break


def harry_plotter():
    fig, ax = plt.subplots()

    # histogram our data with numpy
    data = ping_thing()
    n, bins = np.histogram(data, 100)

    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + n
    nrects = len(left)

    # here comes the tricky part -- we have to set up the vertex and path
    # codes arrays using moveto, lineto and closepoly

    # for each rect: 1 for the MOVETO, 3 for the LINETO, 1 for the
    # CLOSEPOLY; the vert for the closepoly is ignored but we still need
    # it to keep the codes aligned with the vertices
    nverts = nrects*(1+3+1)
    verts = np.zeros((nverts, 2))
    codes = np.ones(nverts, int) * path.Path.LINETO
    codes[0::5] = path.Path.MOVETO
    codes[4::5] = path.Path.CLOSEPOLY
    verts[0::5,0] = left
    verts[0::5,1] = bottom
    verts[1::5,0] = left
    verts[1::5,1] = top
    verts[2::5,0] = right
    verts[2::5,1] = top
    verts[3::5,0] = right
    verts[3::5,1] = bottom

    barpath = path.Path(verts, codes)
    patch = patches.PathPatch(barpath, facecolor='green', edgecolor='yellow', alpha=0.5)
    ax.add_patch(patch)

    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max())


    def animate(i):
        # simulate new data coming in
        data = ping_thing()
        n, bins = np.histogram(data, 100)
        top = bottom + n
        verts[1::5,1] = top
        verts[2::5,1] = top


    ani = animation.FuncAnimation(fig, animate, 100, repeat=False)
    plt.show()





if __name__ == '__main__':
    main()


__author__ = 'todd'
