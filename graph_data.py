"""
Draws the stripcharts as set up on the 'Graph' tab in the main program.
"""

import stuff
import time
import wx
import numpy as np
import matplotlib.pyplot as plt

class DisplayThread(stuff.WorkerThread):
    """
    Plots 'data', a list of numbers, against the list counter, an interger. The
    list 'param' carries all the wx controls including the plotting panel. This
    plotting thread is triggered by a wx timer. It only reads the control settings
    when the thread is started. Depending on how often the thread is run, the
    delay in responding to a changed setting might confuse the user. 
    """    
    def __init__(self, notify_window, EVT, param, data,start_time,Overide):
        stuff.WorkerThread.__init__(self, notify_window, EVT, param, data,start_time,Overide)
        #overide to be ignored, and start time too. can make a new class perhaps
        self.start()

    def run(self):
        xmin_control = self.param[0]
        manual_xmin = self.param[1]
        xmax_control = self.param[2]
        manual_xmax = self.param[3]
        ymin_control = self.param[4]
        manual_ymin = self.param[5]
        ymax_control = self.param[6]
        manual_ymax = self.param[7]
        grid_show = self.param[8]
        label_show = self.param[9]
        panel = self.param[10]
        #access gui directly using wx.CallAfter to put numbers in mean and sd boxes
        mean_box = self.param[11]
        sd_box = self.param[12]
        text_out = self.param[13]#not useable 
        copy_full = list(self.data.value) # a genuine copy, not just a pointer to same list
        window = 50 #default integer number of points plotted in scrolling mode
        #iterate over all the data lists within data.value, should be three of them.
        index = 0 #index in which we are reading
        labels = ['X','Y','Theta']
        for copy in copy_full:
            if len(copy) == 0: #no data so abort the thread
                wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
                return
            else:
                data_stdev = np.std(copy)
            
            if xmax_control=='Auto':
                xmax = len(copy) if len(copy) > window else window
            else:
                try:
                    xmax = int(manual_xmax)
                except ValueError:
                    xmax = window #avoids rubbish in box from stopping the plot
     
            if xmin_control=='Auto':
                xmin = xmax - window
            else:
                try:
                    xmin = int(manual_xmin)
                except ValueError:
                    xmin = 0 #avoids rubbish in GUI box from stopping the plot

            #select points based on xmin and xmax
            points = np.array([float(x) for x in copy[xmin:xmax]])

            theMin = min(points)
            
            if ymin_control=='Auto':
                if data_stdev == '-':#plotting started too early, avoid error due to no stdevv
                    ymin = theMin
                else:
                    ymin = theMin - 0.1*data_stdev
            else:
                try:
                    ymin = float(manual_ymin)#int(self.ymin_control.manual_value())
                except ValueError:
                    ymin = 0 #avoids rubbish in box from stopping the plot
     
            theMax = max(points)
            
            if ymax_control=='Auto':
                if data_stdev == '-':#plotting started too early, avoid error due to no stdevv
                    ymax = theMax
                else:
                    ymax = theMax + 0.1*data_stdev
            else:
                try:
                    ymax = float(manual_ymax)#int(self.ymax_control.manual_value())
                except ValueError:
                    ymax = 100 #avoids rubbish in box from stopping the plot

            panel.axs[index].plot(np.arange(xmin,xmin+len(points),1),points,'r')
            panel.axs[index].xlabel(labels[index])
            #then window in on what is required...probably inefficient
            #panel.axs[index].set_xbound(lower = xmin, upper = xmax)
            #panel.axs[index].set_ybound(lower = ymin, upper = ymax)
            
            if grid_show:
                panel.axs[index].grid(True, color='white')
            else:
                panel.axs[index].grid(False)
            plt.setp(panel.axs[index].get_xticklabels(),visible=label_show)
     
            

            if self._want_abort: #abort not useful for this single run thread
                wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
                return
    ##         wx.CallAfter(text_out.AppendText,'Plotting finished\n')
            wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, '..plotted'))
            index = index + 1 #go to the next subplot

        panel.canvas.draw()

