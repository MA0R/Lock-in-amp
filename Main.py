"""
Main thread for controlling the buttons of the ref-step algorithm
"""
import wx, wx.html
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys
import time
import os

import visa2 # this is the simulation version of visa
import visa

import noname #The inherited class for GUI
import gpib_data #Data collection thread
import instrument #General instrument class
import stuff #Extra functions and things that dont have a home yet
import graph_data #graphing thread
import pywxgrideditmixin #mixin to allow copy and paste from/to tables
import tables #For printing tables and stuff

import inst_ch
import inst_lock_in
import inst_meter
import inst_attenuator

class GraphFrame(noname.MyFrame1):
    def __init__(self, parent):
        noname.MyFrame1.__init__(self, parent)
        #the mixin below offers better ctrl c ctr v cut and paste than the basic wxgrid
        wx.grid.Grid.__bases__ += (pywxgrideditmixin.PyWXGridEditMixin,)
        self.m_grid3.__init_mixin__()
        self.number_plots = 3
        self.CreateGraph('time', self.number_plots)
        self.m_button2.SetLabel('Plot') #starts with plotting off
        self.paused = True
        self.Show(True)
        # Define notification event for thread completion
        self.EVT_RESULT_ID_0 = wx.NewId() #used for graphing thread
        self.EVT_RESULT_ID_1 = wx.NewId() #used for GPIB data 1 thread
        self.worker0 = None # for graphing
        self.worker1 = None # for data source 1
        stuff.EVT_RESULT(self, self.OnResult0, self.EVT_RESULT_ID_0)
        stuff.EVT_RESULT(self, self.OnResult1, self.EVT_RESULT_ID_1)
        log = self.m_textCtrl81 # where stdout will be redirected
        redir = stuff.RedirectText(log)
        sys.stdout = redir #print statements, note to avoid 'print' if callafter delay is an issue
        sys.stderr = redir #python errors
        self.data = stuff.SharedList(None) #no data on start up
        self.timer0 = wx.Timer(self) #a timer for regular graphing
        self.Bind(wx.EVT_TIMER, self.OnTimer0, self.timer0) # bind to OnTimer
        self.m_checkBox1.SetValue(True) #show grid
        self.m_checkBox2.SetValue(True) #show x labels
        self.cwd = os.getcwd() #identifies working directory at startup.
        iconFile = os.path.join(self.cwd, 'testpoint.ico')
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.dirname = 'xxx'
        self.SetIcon(icon1)
        self.inst_bus = visa # can be toggled (OnSimulate) to visa 2 for simulation
        self.START_TIME = 0 #to be overidden when worker thread is called
        self.filled_grid = False #was grid sucessfuly filled
        self.loaded_dict = False
        self.loaded_ranges = False
        self.OverideSafety = False
        self.controlgrid = tables.TABLES(self)

        ########################
        # disable some bottons #
        ########################
        

    def CreateGraph(self, xlabel, number):
        """
        #number is the number of subplots to be created
        Not clear how we auto scale all the axes if there are many subplots
        """
        #Note use of pyplot for convenient subplots. Could be done in other ways.
        panel = self.m_panel61
        panel.dpi = 100
        if number == 1:
            share = False
        else:
            share = True
        panel.fig, panel.axs = plt.subplots(number, 1, sharex=share, sharey=False)
        graph_title = 'Instrument Output'
        if number == 1:
            panel.axs.set_title(graph_title)
            panel.axs.set_axis_bgcolor('LightBlue')
            panel.axs.grid(True, color='white')
            panel.axs.tick_params(axis = 'both', labelsize=8)
        else:
            panel.axs[0].set_title(graph_title)
            for i in range(number):
                panel.axs[i].set_axis_bgcolor('blue')
                panel.axs[i].grid(True, color='white')
                panel.axs[i].tick_params(axis='both', labelsize=8)
        panel.fig.tight_layout()
        panel.canvas = FigureCanvas(panel, -1, panel.fig)
        panel.sizer = wx.BoxSizer(wx.VERTICAL)
        panel.sizer.Add(panel.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        panel.SetSizer(panel.sizer)
        panel.Fit()
        self.add_2Dtoolbar(panel)
        self.m_scrolledWindow1.SendSizeEvent()

    def add_2Dtoolbar(self, panel):
        """
        Adds the standard matplotlib toolbar that provides extra viewing
        features (e.g., pan and zoom).
        """
        panel.toolbar = NavigationToolbar2WxAgg(panel.canvas)
        panel.toolbar.Realize()
        tw, th = panel.toolbar.GetSizeTuple()
        fw, fh = panel.canvas.GetSizeTuple()
        panel.toolbar.SetSize(wx.Size(fw, th))
        panel.sizer.Add(panel.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        panel.toolbar.update()
        panel.SendSizeEvent()

    def OnLive(self, event):
        """
        Chooses visa for live instruments
        """
        if self.m_menuItem2.IsChecked():
            self.inst_bus = visa #default for real instruments

    def OnSimulate(self, event):
        """
        Chooses visa2 for simulated (poorly) GPIB.
        """
        if self.m_menuItem1.IsChecked():
            self.inst_bus = visa2 #choose visa2 for simulation

    def OnOpenDict(self, event):
        """
        from MIEcalculator, graph_gui.py.
        """
        # In this case, the dialog is created within the method because
        # the directory name, etc, may be changed during the running of the
        # application. In theory, you could create one earlier, store it in
        # your frame object and change it when it was called to reflect
        # current parameters / values
        wildcard = "Poject source (*.csv; *.xls; *.xlsx; *.xlsm)|*.csv;*.xls; *.xlsx; *.xlsm|" \
         "All files (*.*)|*.*"

        dlg = wx.FileDialog(self, "Choose a project file", self.dirname, "", \
        wildcard, wx.OPEN | wx.MULTIPLE)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            self.proj_file = os.path.join(dirname, filename)
            self.projwd = dirname #remember the project working directory
            self.FillGrid()
        dlg.Destroy()

    def OnLoadTable(self, event):
        self.FillGrid()

    def FillGrid(self):
        """
        Loads self.proj_file to the grid. Requires a dictionary sheet named "Dict" and
        a control sheet named "Control". Uses tables.TABLES for a excel-to-grid object.
        Need to change from try-except to a structure that returns a failure if the grid was
        not sucessfully loaded. This would then better pin point errors, since try-except
        simply does the exception if it came to an error. 
        """

        
        #note passing self is not ideal, pass the scroll window instead

        self.filled_grid = self.controlgrid.excel_to_grid(self.proj_file, 'Control', self.m_grid3)
        if self.filled_grid == True:
            grid = self.m_grid3
            if int(float(grid.GetCellValue(3, 3))) > int(grid.GetNumberRows()):
                #int(float( is needed as it cant seem to cast straight to an int
                print("Final row needed to be updated in grid")
                grid.SetCellValue(3, 3, str(grid.GetNumberRows()))
        else:
            print("no sheet named 'Control' found")

    def OnAnalysisFile(self, event):
        """
        from MIEcalculator, graph_gui.py.
        """
        # In this case, the dialog is created within the method because
        # the directory name, etc, may be changed during the running of the
        # application. In theory, you could create one earlier, store it in
        # your frame object and change it when it was called to reflect
        # current parameters / values
        wildcard = "Poject source (*.csv; *.xls; *.xlsx; *.xlsm)|*.csv;*.xls; *.xlsx; *.xlsm|" \
         "All files (*.*)|*.*"

        dlg = wx.FileDialog(self, "Choose a project file", self.dirname, "",\
        wildcard, wx.OPEN | wx.MULTIPLE)
        analysis_file = None

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            analysis_file = os.path.join(dirname, filename)
        dlg.Destroy()
        if analysis_file: self.Analysis_file_name.SetLabel(analysis_file)

    def OnAnalyse(self, event):
        pass

    def OnSaveTables(self, event):
        """
        from MIEcalculator, graph_gui.py.
        """
        # In this case, the dialog is created within the method because
        # the directory name, etc, may be changed during the running of the
        # application. In theory, you could create one earlier, store it in
        # your frame object and change it when it was called to reflect
        # current parameters / values
        wildcard = "Poject source (*.csv; *.xls; *.xlsx; *.xlsm)|*.csv;*.xls; *.xlsx; *.xlsm|" \
         "All files (*.*)|*.*"

        dlg = wx.FileDialog(self, "Choose a project file", self.dirname, "",\
        wildcard, wx.OPEN | wx.MULTIPLE)

        save_file = None

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            save_file = os.path.join(dirname, filename)
        dlg.Destroy()
        if save_file: self.SaveGrid(save_file)

    def SaveGrid(self, path):
        """
        Saves using the tables.TABLES object
        """
        #not saving "ranges", this is a specific product
        self.controlgrid.grid_to_excel(path, [(self.m_grid3, "Control"), (self.m_grid2, "Dict")])

    def DoReset(self, event):
        """
        Resets by clearing the data, and clearing the on screen text feedback.
        Also sets the Make Safe button back to green.
        """
        #reset the data, and clear the text box
        self.doStop()
        self.data.reset_list()
        self.m_textCtrl81.Clear()
        self.m_button12.SetBackgroundColour(wx.Colour(0, 255, 0))

    def OnStart(self, event):
        """
        Creates the instruments, and calls the doStart function.
        """
        if self.filled_grid == True:
            self.CreateInstruments()
            self.doStart()

    def CreateInstruments(self):
        """
        Sends the instrument bus (visa or visa2), letter (For instrument type) and adress
        to instrument objects and saves them as class variables.
        """
        
        self.lcin = inst_lock_in.LOCK_IN(self.inst_bus,'L', self.LcinAdress.GetValue())
        self.meter = inst_meter.METER(self.inst_bus,'M', self.MeterAdress.GetValue())
        self.source = inst_ch.CLARKE_HESS(self.inst_bus,'S', self.SourceAdress.GetValue())
        self.atten = inst_attenuator.ATTENUATOR(self.inst_bus,'A', self.AttenAdress.GetValue())

    def OnOverideSafety(self, event):
        self.OverideSafety = True

    def OnCompleteChecks(self, event):
        self.OverideSafety = False

    def doStart(self):
        """
        Starts the algorithm, sends the created instruments to the wroker thread.
        """
        #self.meter,self.sourceS,self.sourceX = instruments
        #first read essential setup info from the control grid (self.m_grid3).
        grid = self.m_grid3
        grid.EnableEditing(False)
        #int(float()) is needed because the grid has loaded,e.g. 2.0 instead of 2
        start_row = int(float(grid.GetCellValue(3, 1)))-1#wxgrid starts at zero
        stop_row = int(float(grid.GetCellValue(3, 3)))-1
        cols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.START_TIME = time.localtime()

        #HIDE BUTTONS
        for button in [self.m_menuItem21, self.m_menuItem11, self.m_menuItem111, self.m_menuItem2,\
        self.m_menuItem1, self.m_menuItem25, self.m_menuItem26, self.m_button15, self.m_button16]:
            button.Enable(False)

        #now call the thread
        if not self.worker1:
            self.worker1 = gpib_data.GPIBThreadF(self, self.EVT_RESULT_ID_1,\
            [self.inst_bus, grid, start_row, stop_row, self.lcin, self.meter, self.source, self.atten, cols],\
            self.data, self.START_TIME, self.OverideSafety) #self.Analysis_file_name sent too?

    def OnStop(self, event):
        self.doStop()

    def doStop(self):
        """
        Flags the worker thread to stop running if it exists.
        """
        # Flag the worker thread to stop if running
        if self.worker1:
            print('Halting GPIB data gathering')
            self.worker1.abort()

    def OnMakeSafe(self, event):
        """
        Flags all threads to stop.
        """
        self.doStop() #stop main data gathering
        self.timer0.Stop()#graph timer is stopped
        self.paused = True #graphing is paused
        self.m_button2.SetLabel("Plot")

        # next run a gpib thread that sets sources to zero and standby and meter to autorange HV?

    def OnTimer0(self, evt):
        self.thePlot()

    def OnPauseButton(self, event):
        if self.paused:
            self.thePlot #plot immediately, then on timer events
            self.timer0.Start(1000)
        else:
            self.timer0.Stop()
        self.paused = not self.paused
        label = "Plot" if self.paused else "Pause"
        self.m_button2.SetLabel(label)

    def OnResult0(self, event):
        """Show Result status, event for termination of graph thread"""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            #print'Plotting aborted', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            self.m_textCtrl14.AppendText('Plotting aborted ')
            self.m_textCtrl14.AppendText(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
            self.m_textCtrl14.AppendText('\n')
        else:
            # Process results here
            self.m_textCtrl14.AppendText('Plot ended ')
            self.m_textCtrl14.AppendText(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
            self.m_textCtrl14.AppendText('\n')
        # In either event, the worker is done
        self.worker0 = None

    def OnResult1(self, event):
        """Show Result status, event for termination of gpib thread"""

        #ENABLE BUTTONS
        for button in [self.m_menuItem21, self.m_menuItem11, self.m_menuItem111, self.m_menuItem2, self.m_menuItem1,\
        self.m_menuItem25, self.m_menuItem26, self.m_button15, self.m_button16]: button.Enable(True)

        if event.data is None:
            # Thread aborted (using our convention of None return)
            print('GPIB data aborted'), time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        else:
            # Process results here
            print('GPIB Result: %s' % event.data, time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
            if event.data == "UNSAFE":
                self.m_button12.SetBackgroundColour(wx.Colour(255, 0, 0))

        # In either event, the worker is done
        self.worker1 = None
        self.m_grid3.EnableEditing(True)

    def thePlot(self):
        params = []
        #read all the graph GUI settings to put into params

        xmin_control = self.m_radioBox1.GetStringSelection()
        manual_xmin = self.m_textCtrl2.GetValue()
        xmax_control = self.m_radioBox2.GetStringSelection()
        manual_xmax = self.m_textCtrl3.GetValue()

        ymin_control = self.m_radioBox3.GetStringSelection()
        manual_ymin = self.m_textCtrl4.GetValue()
        ymax_control = self.m_radioBox4.GetStringSelection()
        manual_ymax = self.m_textCtrl5.GetValue()
        show_grid = self.m_checkBox1.IsChecked()
        show_labels = self.m_checkBox2.IsChecked()

        params.append(xmin_control)
        params.append(manual_xmin)
        params.append(xmax_control)
        params.append(manual_xmax)
        params.append(ymin_control)
        params.append(manual_ymin)
        params.append(ymax_control)
        params.append(manual_ymax)
        params.append(show_grid)
        params.append(show_labels)

        params.append(self.m_panel61)
        #maybe unwise to paass these to thread?
        params.append(self.m_textCtrl121)
        params.append(self.m_textCtrl13)
        params.append(self.m_textCtrl14)#for displaying plot events

        if not self.worker0:
            self.worker0 = graph_data.DisplayThread(self, self.EVT_RESULT_ID_0, params, self.data, self.START_TIME, None)

    def OnGetInstruments(self, event):
        rm = self.inst_bus.ResourceManager()#new Visa
        try:
            #check = self.inst_bus.get_instruments_list()
            check = rm.list_resources()#new Visa
        except self.inst_bus.VisaIOError:
            check = "visa error"
        self.m_textCtrl8.SetValue(repr(check))
        self.m_panel7.SendSizeEvent()#forces textCtrl8 to resize to content

    def OnRefreshInstruments(self, event):
        """
        Adds all active instrument adresses to the drop down selection for the instrumetns.
        """
        rm = self.inst_bus.ResourceManager()#new Visa
        try:
            resources = rm.list_resources()
            self.LcinAdress.Clear()
            self.MeterAdress.Clear()
            self.SourceAdress.Clear()
            self.AttenAdress.Clear()
            for adress in resources:
                self.LcinAdress.Append(adress)
                self.MeterAdress.Append(adress)
                self.SourceAdress.Append(adress)
                self.AttenAdress.Append(adress)

        except self.inst_bus.VisaIOError:
            resources = "visa error"
        #self.m_textCtrl8.SetValue(repr(check))


    def OnInterfaceClear(self, event):
        rm = self.inst_bus.ResourceManager()#new Visa
        #self.inst_bus.Gpib().send_ifc()
        bus = rm.open_resource('GPIB::INTFC')#opens the GPIB interface
        bus.send_ifc()

    def OnSendTestCommand(self, event):
        """
        Sends a test command to the selected instrument using doSend.
        """
        
        instrument = self.m_comboBox8.GetValue()
        if instrument == 'Lock in':
            adress = self.LcinAdress.GetValue()
            self.doOnSend(adress)
        elif instrument == 'meter':
            adress = self.MeterAdress.GetValue()
            self.doOnSend(adress)
        elif instrument == 'Source':
            adress = self.SourceAdress.GetValue()
            self.doOnSend(adress)
        elif instrument == 'Attenuator':
            adress = self.AttenAdress.GetValue()
            self.doOnSend(adress)
        else:
            self.m_textCtrl23.AppendText('select instrument\n')

    def doOnSend(self, adress):
        """ sends the commend to the adress specified, creates a new visa resource manager."""

        command = self.m_textCtrl18.GetValue()
        rm = self.inst_bus.ResourceManager()#new Visa
        instrument = rm.open_resource(adress)
        instrument.write(command)
        self.m_textCtrl23.AppendText(command+'\n')

    def OnReadTestCommand(self, event):
        """
        Reads from whatever instrument is selected using doRead.
        Will fail if it finds nothing on the instrument bus.
        """
        instrument = self.m_comboBox8.GetValue()
        if instrument == 'Lock in':
            adress = self.LcinAdress.GetValue()
            self.doRead(adress)
        elif instrument == 'meter':
            adress = self.MeterAdress.GetValue()
            self.doRead(adress)
        elif instrument == 'Source':
            adress = self.SourceAdress.GetValue()
            self.doRead(adress)
        elif instrument == 'Attenuator':
            adress = self.AttenAdress.GetValue()
            self.doRead(adress)
        else:
            self.m_textCtrl23.AppendText('select instrument\n')

    def doRead(self, adress):
        """reads from the specified adress"""
        rm = self.inst_bus.ResourceManager()#new Visa
        instrument = rm.open_resource(adress)
        try:
            value = instrument.read_raw()
            self.m_textCtrl23.AppendText(repr(value)+'\n')
            return
        except self.inst_bus.VisaIOError:
            self.m_textCtrl23.WriteText('Failed to get reading from instrument\n')
            return

    def OnHelp(self, event):
        print("showing help")
        dlg = HelpBox(None)
        html = dlg.m_htmlWin1
        name = 'help.html'
        html.LoadPage(name)
        dlg.Show()

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info = wx.AboutDialogInfo()
        info.SetName('Ref stepr')
        info.SetVersion('1.0.0')
        info.SetDescription("description")
        info.SetCopyright('(C) 2017-2018 Measurement Standards Laboratory of New Zealand')
        info.SetWebSite('http://www.msl.irl.cri.nz')
        info.SetLicence("who knows")
        info.AddDeveloper('some code maker')
        wx.AboutBox(info)


    def OnClose(self, event):
        """
        Make sure threads not running if frame is closed before stopping everything.
        Seems to generate errors, but at least the threads do get stopped!
        The delay after stopping the threads need to be longer than the time for
        a thread to normally complete? Since thread needs to be able to post event
        back to the main frame.
        """
        if self.worker1: #stop main GPIB thread
            self.worker1.abort()
            time.sleep(0.3)
        if self.worker0: #stop graph timer and plotting
            self.timer0.Stop()
            self.worker0.abort()
            time.sleep(1.1)#minimises error messages from suddenly stopped graph
        self.Destroy()

        
###########################################################################
## Class HelpFrame
###########################################################################

class HelpBox ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        gbSizer4 = wx.GridBagSizer( 0, 0 )
        gbSizer4.SetFlexibleDirection( wx.BOTH )
        gbSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_htmlWin1 = wx.html.HtmlWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 1500,1250 ), wx.html.HW_SCROLLBAR_AUTO )
        gbSizer4.Add( self.m_htmlWin1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


        self.SetSizer( gbSizer4 )
        self.Layout()
        self.Centre( wx.BOTH )

    def __del__( self ):
        pass
	
	
	


if __name__ == "__main__":
    app = wx.App()
    GraphFrame(None)
    app.MainLoop()
