"""
Everything about GPIB control for the Ref Step algorithm.
The GUI should only allow one GPIB thread at a time.
Thread also writes raw data file to an excel sheet.
Log files are written at event termination from graphframe.py.
"""

import stuff
import csv
import time
import wx
import visa #use inst_bus instead of visa so the calling application
#can provide the simulated (visa2) or real version of visa
import visa2
import numpy as np
import gpib_inst
import openpyxl
import Thread as Swerlein

class GPIBThreadF(stuff.WorkerThread):
    """
    Ref step main thread
    """
    def __init__(self, notify_window, EVT, param, data, start_time, OverideSafety):
        stuff.WorkerThread.__init__(self, notify_window, EVT, param, data, start_time, OverideSafety)
        #param[0] holds self.inst_bus, the chosen real or simulated visa
        self.inst_bus = param[0] #visa or simulated visa2
        self.grid = param[1]
        self.start_row = param[2]
        self.stop_row = param[3]

        self.lcin = param[4]
        self.meter = param[5]
        self.source = param[6]
        self.atten = param[7]

        self.VarV_col, self.Phase_col, self.RefV_col, self.MeasRef_col, self.AutoPhase_col, self.Reserve_col, self.Freq_col,\
        self.Atten_col, self.lcin_phase_col, self.meter_range_col, self.nordgs_col = param[8]
        #columns to print to:
        self.ref_v_print = 13
        self.sr_x_print = 14
        self.sr_y_print = 16
        self.sr_range_print = 18
        self.time_const_print = 19
        self.sr_theta_print = 20
        self.sr_res_mod_print = 21
        self.sr_auto_phas_print = 22
        
        self.OverideSafety = OverideSafety
        self.MadeSafe = False

        log_file_name = 'log.'+str(start_time[0])+'.'+str(start_time[1])+'.'+str(start_time[2])+'.'+str(start_time[3])+'.'+str(start_time[4])+".txt"
        self.raw_file_name = 'raw.'+str(start_time[0])+'.'+str(start_time[1])+'.'+str(start_time[2])+'.'+str(start_time[3])+'.'+str(start_time[4])
        self.wb = openpyxl.Workbook()
        self.sh = self.wb.active
        self.logfile = open(log_file_name, 'w')
        first_line = [self.read_grid_cell(6, i) for i in range(self.grid.GetNumberCols())]+['start time', 'end time', 'readings...']

        for i in range(6):
            self.sh.append([self.read_grid_cell(i, column) for column in range(10)])
            #append empty things, but they can contain more useful info later
            #dates, instruments, start time finish time?
            #This skeeps the analysis sheets compatible with the normal input files.
        self.sh.append(first_line)

        self.rm = self.inst_bus.ResourceManager() #one resource manager for this thread
        self.com(self.lcin.create_instrument) #create lcin in resource manager, before thread start
        self.com(self.meter.create_instrument) #create meter
        self.com(self.source.create_instrument)
        self.com(self.atten.create_instrument)
        
        self.start() #important that this is the last statement of initialisation. goes to run()

    def PrintSave(self, text):
        """
        Prints a string, and saves to the log file too.
        """
        if self._want_abort: #stop the pointless printing if the thread wants to abort
            return
        else:
            self.logfile.write(str(text)+"\n")
            print(str(text))

    def MakeSafe(self):
        """
        MakeSafe executes the make safe commands straight to the instruments,
        bypassing the try_command structure.
        Incase it it failed making safe, the Make safe button will turn red
        (posts "UNSAFE" to the main thread) and state which instruments the make safe failed at.
        The program only attempts the make safe once and terminates the thread.
        """
        if self.MadeSafe == False:
            sucess = True
            #executes the make safe sequence on each instrument, bypassing the try_command
            insts = [self.lcin.com['label'], self.meter.com['label'], self.source.com['label']]
            #lcin label, meter label, source label
            safes = [self.lcin.com['MakeSafe'], self.meter.com['MakeSafe'], self.source.com['MakeSafe']]
            #make ssafe routines for each
            for l,s in zip(insts, safes):
                try:
                    exec('self.'+str(l)+'.write("'+str(s)+'")')
                except self.inst_bus.VisaIOError:
                    sucess = False
                    self.PrintSave("DID NOT SUCESFULLY MAKE "+str(l)+" SAFE")
            if sucess == False:
                wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, "UNSAFE"))
            else:
                wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))

        self.MadeSafe = True

    def com(self, command,value=None):
        if not self._want_abort:
            if value != None:
                return command(value)
            else:
                return command()
        else:
            return 0


    def Error_string_maker(self):
        """
        Reads all errors in the instruments, and appends them together in a string.
        If there are errors during the running of the code, they will be printed
        on the left of the table as a warning flag.
        """
        #somehow still prints "0" when the instruments have no error.
        string = " "
        #query instrument errors, and save individual error strings.
        self.com(self.meter.query_error)
        m_esr = str(self.com(self.meter.read_instrument))
        self.PrintSave('meter ESR = '+m_esr)
        if m_esr != self.meter.com['NoError']: string = 'meter: '+m_esr
        self.com(self.source.query_error)
        s_esr = str(self.com(self.source.read_instrument))
        self.PrintSave('source ESR = '+s_esr)
        if s_esr != self.source.com['NoError']: string = string +' source : '+s_esr
        self.com(self.lcin.query_error)
        l_esr = str(self.com(self.lcin.read_instrument))
        self.PrintSave('lcin ESR = '+l_esr)
        if l_esr != self.lcin.com['NoError']: string = string +' lcin: ' +l_esr

        return string

    def set_attenuation(self, row):
        """
        Attenuation is set here, soon to set the number of readings too?
        """
        case = self.read_grid_cell(row, self.Atten_col)
        
        case = int(float(case)) #attenuation col has 1 for setting attenuation
        if case == 0:
            self.com(self.atten.set_value,"B123\\\\nB567")
        elif case == 20:
            self.com(self.atten.set_value,"A2B13\\nB567")
        elif case == 40:
            self.com(self.atten.set_value,"A3B12\\nB567")
        elif case == 60:
            self.com(self.atten.set_value,"A23B1\\nB567")
        elif case == 80:
            self.com(self.atten.set_value,"A3B12\\nA7B56")
        elif case == 100:
            self.com(self.atten.set_value,"A23B1\\nA7B56")
        elif case == 120:
            self.com(self.atten.set_value,"A23B1\\nA67B5")
        else:
            self.PrintSave("No valid attentuation")

    def set_voltage_phase(self, row):
        """
        Function to set the voltage
        """
        self.com(self.source.set_value,self.command(row, self.Freq_col))
        self.com(self.source.set_value,self.command(row, self.Atten_col))#but this one wont have the correct header...
        self.com(self.source.set_value,self.command(row, self.VarV_col))
        self.com(self.source.set_value,self.command(row, self.Phase_col))

    def run_swerl(self, row):
        """
        start the swerlein algorithm, perhaps seperate thread?
        """
        if int(float(self.read_grid_cell(row, self.MeasRef_col)))==1: #conditions on when to run swerlein, if there is anything in the box
            self.swerl = Swerlein.Algorithm(port = 24) #sets the thread running.
            loop = True
            while loop == True:
                if self.swerl.ready == True:
                    acdcrms = self.swerl.All_data[0][2] #loop ends here and function returns the acdcrms readings
                    self.set_grid_val(row,self.ref_v_print,acdcrms)
                    loop = False
                if self._want_abort:
                    loop = False
            print(self.swerl.All_data)
        
    def set_grid_val(self,row,col,data):
        wx.CallAfter(self.grid.SetCellValue, row, col, str(data))
        
    def read_grid_cell(self,row,col):
        if not self._want_abort:
            value = self.grid.GetCellValue(row, col)
            return value

    def set_up_lcin(self, row):
        """
        read the reserve and range cells, and send with appropriate packaging
        """
        self.com(self.lcin.set_value, self.command(row, self.Reserve_col))
        self.com(self.lcin.set_value,self.command(row, self.lcin_phase_col))
        #   WHAT IS THE RANGE THAT IT GETS SENT?

    def command(self, row, col):
        """
        given a row and column, it will return the full command to send the instrument.
        The command has the column header decorating the actual value, value replaces "$".
        """
        val = str(self.read_grid_cell(row, col))
        com = str(self.read_grid_cell(self.start_row-1, col)) #reads column headers
        return com.replace("$",val)


    def run(self):
        """
        Main thread, reads through the table and executes commands.
        """
        ####################INITIALISE INSTRUMENTS##########################

        self.com(self.lcin.reset_instrument) #reset lcin
        self.com(self.source.reset_instrument)
        self.com(self.meter.reset_instrument)
        time.sleep(3)
        self.com(self.lcin.initialise_instrument) #initialise the lcin for reading
        self.com(self.meter.initialise_instrument)
        self.com(self.source.initialise_instrument)
        #error string for source?

        self.PrintSave('')
        self.com(self.meter.query_error)
        self.PrintSave('meter ESR = '+str(self.com(self.meter.read_instrument)))
        self.com(self.source.query_error)
        self.PrintSave('source ESR = '+str(self.com(self.source.read_instrument)))
        self.com(self.lcin.query_error())
        self.PrintSave('meter ESR = '+str(self.com(self.lcin.read_instrument)))
        self.PrintSave('')

            ##read all instruments status and print

        ######################END of INITIALISATION##########################

        ######################MEASUREMENT PROCESS############################

        for row in range(self.start_row, self.stop_row + 1):
            #read all the values in the line.

            self.PrintSave("Spread sheet row "+str(int(row)+1))
            wx.CallAfter(self.grid.SelectRow, row)
            wx.CallAfter(self.grid.ForceRefresh)
            wx.CallAfter(self.grid.Update)

            self.set_attenuation(row)

            self.set_voltage_phase(row)
             
            self.run_swerl(row)
            #measurement settings, and DVM range setting
            nordgs = int(float(self.read_grid_cell(row, self.nordgs_col)))

            self.set_up_lcin(row)
            self.com(self.source.MeasureSetup)
            self.com(self.lcin.MeasureSetup)
            x_readings = []
            y_readings = []
            t_readings = []
            before_msmnt_time = time.time() #start time of measuremtns.
            for i in range(nordgs):
                #where to add the "if not self.want_abort:"?
                #idea is to stop the tripple reading from attempting to break up an int,
                #otherwise python crashes, its not a safe stopping of the program.
                self.com(self.source.SingleMsmntSetup) #?
                self.com(self.lcin.SingleMsmntSetup)
                time.sleep(3)
                tripple_reading = str(self.com(self.lcin.read_instrument))
                print(tripple_reading)
                #x, y, t = tripple_reading.split(",")
                if not self._want_abort:
                    x,y,t = str("{},{},{}".format(self.com(self.lcin.read_instrument),self.com(self.lcin.read_instrument),self.com(self.lcin.read_instrumen))).split(",")
                    #will have to split the row at "," or whatever NEED TO WORK IT OUT
                    x_readings.append(float(x))
                    y_readings.append(float(y))
                    t_readings.append(float(t))
            
            printing_cols = [self.sr_range_print,self.sr_res_mod_print,self.sr_res_mod_print,self.sr_auto_phas_print]
            self.com(self.lcin.set_value,"SENS?;RMOD?;OFLT?;PHAS?\\\\n")
            for col in printing_cols:
                self.set_grid_val(row,col,str(self.com(self.lcin.read_instrument)))
            
            #the readings would be empty arrays if the program is sent to stop, then the values returned will be "nan".
            self.set_grid_val(row,self.sr_x_print,np.average(x_readings))
            self.set_grid_val(row,self.sr_x_print+1,np.std(x_readings))
            self.set_grid_val(row,self.sr_y_print,np.average(y_readings))
            self.set_grid_val(row,self.sr_y_print+1,np.std(y_readings))
            self.set_grid_val(row,self.sr_theta_print,"{},{}".format(np.average(t_readings),np.std(t_readings)))
        #unused columns?
        #self.sr_range_print = 19
        #self.time_const_print = 20

        
        ####################### END of MEASUREMENT PROCESS #####################

