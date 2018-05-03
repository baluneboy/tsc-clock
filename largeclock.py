#!/usr/bin/env python

"""Use Tkinter to show a large digital clock."""

# 8/20/2015 Hrovat modified to allow for input arguments
# 9/1/2015  Hrovat modified for white bg when yoda db problem
# 4/30/2018 Hrovat modified to get rid of global
# 5/3/2018  Hrovat revised to get rid of numpy (because py2exe issue on trek) and incorporate new LOS indicator strategy

import os
import sys
import time
import math
import datetime
#import numpy as np
import ConfigParser
from Tkinter import *
from multiprocessing import Queue

from db import query_aos
from fifo import TimeCheckableFifo

#from pims.largeclock.timeout import run_with_timeout

_PWORD = raw_input('samsops pword: ') # USE TEMPORARY HARD-CODED FOR PY2EXE

        
# get path to this script; used to find largeclock.cfg (config) file
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


# if no input args, then we try to read cfg file (fallback to hard-coded values)
def get_config():
    if len(sys.argv) == 1:
        try:
            # attempt to read local config file
            #script_path = get_script_path()
            #config_file = os.path.join(script_path, "largeclock.cfg")
            if os.name is 'posix':
                script_path = get_script_path()
                config_file = os.path.join(script_path, "largeclock.cfg")
            else:
                config_file = r"C:\\largeclock\\largeclock.cfg"               
            config = ConfigParser.ConfigParser()
            config.read(config_file)
            font_size = int( config.get('font', 'size') )
            w = int( config.get('window', 'width') )
            h = int( config.get('window', 'height') )
            _default = config.get('timeformat', 'default')
            _custom = config.get('timeformat', 'custom')
        except:
            font_size = 180 # font size
            w, h = 1500, 200 # width and height of Tk root window
            _default='%Y-%m-%d, %j/%H:%M:%S'
            _custom='%Y:%j:%H:%M:%S'
    else:
        font_size = int(sys.argv[1])
        w = int(sys.argv[2])
        h = int(sys.argv[3])
        _default = sys.argv[4]
        _custom = sys.argv[5]
   
    return font_size, w, h, _default, _custom


# get query results for Ku AOS/LOS with timeout
def get_aos_query_results_with_timeout(_PWORD):
    timeout_sec = 3
    out_q = Queue()
    args = (_PWORD, out_q)
    kwargs = {}
    finished = run_with_timeout(query_aos, timeout_sec, args, kwargs)
    if finished:
        if out_q.empty():
            return None, None
        else:
            return out_q.get()
    else:
        return None, None  # hit the timeout


# update every wait_ms (msec)
def tick(buff, wait_ms):

    # get array of deltas from FIFO buffer
    # for t in buff: print t
    deltas = buff.get_deltas()
    
    # compute sum of deltas (from FIFO buffer) to assess AOS/LOS
    #sum_deltas = np.sum(buff.get_deltas())
    sum_deltas = sum(buff.get_deltas())
    # print sum_deltas
    # print '-' * 22

    time1 = buff[-1].strftime('%j  %H:%M:%S')

    # get the current local time from local machine
    time2 = datetime.datetime.now().strftime('%j  %H:%M:%S')

    # if time string has changed, update it
    # with label update once per second
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)

        ku_timestamp, ku_aos_los = query_aos(_PWORD)
        buff.append(ku_timestamp)

        # every odd # seconds (every other second), check if AOS/LOS and
        # update color & title text
        if int(time2[-1:]) % 2:
                
            if ku_timestamp:
                ku_time = ku_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                # if ku_aos_los:
                #     clock.config(bg='green')
                # else:
                #     clock.config(bg='yellow')
                if sum_deltas == 0:
                    clock.config(bg='yellow')
                elif sum_deltas < 3:
                    clock.config(bg='green')
                else:
                    clock.config(bg='pale green')
            else:
                ku_time = "yoda db connection error"
                clock.config(bg='white')
            root.title( 'ku_timestamp = %s' %  ku_time)

    # now call tick every 200 milliseconds to update display
    clock.after(wait_ms, tick, buff, wait_ms)


# menu callback for copying time to clipboard
def menu_callback(fmt):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(datetime.datetime.now().strftime(fmt))
    r.destroy()


if __name__ == "__main__":   
    
    # get font size, window width, and window height
    font_size, w, h, _default, _custom = get_config()
    
    # get root window and screen dimensions
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # compute x and y coords for root window
    x = (screen_width/2) - (w/2)
    y = (screen_height/2) - (h/2)
    
    # set root window size and position
    geom = '%dx%d+%d+%d' % (w, h, x, y)
    root.geometry( geom )
    
    # create popup menu
    menu = Menu(root, tearoff=0)
    menu.add_command(label="CopyDefault", command=lambda: menu_callback(_default))
    menu.add_command(label="CopyCustom", command=lambda: menu_callback(_custom))   
    
    def popup(event):
        menu.post(event.x_root, event.y_root)    
    
    # initialize time, color, and clock label before main loop
    time1 = datetime.datetime(1970, 1, 1)
    clock = Label(root, font=('arial', font_size, 'bold'), bg='white')
    clock.pack(fill=BOTH, expand=1)
    clock.bind("<Button-3>", popup)

    # NOTE: do not make fifo_len too short (keep it greater than 5 for msec_wait = 200)
    
    # get time now, do first tick, and start main loop
    msec_wait = 200  # how long to wait (msec) between calls to main "tick" update routine
    fifo_len_sec = 1.2  # length of fifo buffer used to gauge AOS/LOS
    #fifo_len = int(np.ceil(1000.0 * fifo_len_sec / msec_wait))  # length of fifo buffer
    fifo_len = int(math.ceil(1000.0 * fifo_len_sec / msec_wait))  # length of fifo buffer
    print 'fifo_len =', fifo_len
    fifo = TimeCheckableFifo([time1] * fifo_len, fifo_len)
    tick(fifo, msec_wait)
    root.mainloop()
