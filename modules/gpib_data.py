"""
Everything about GPIB control for the lockin calibration algorithm.
The GUI should only allow one GPIB thread at a time.
Thread also writes raw data file to an excel sheet.
Log files are written at event termination from graphframe.py.

The "com" function ends up being a little clunky, this was originally developed
for refstep where everything had to be very safe so it made sense to wrap
each command with a safety check. A function decorator can be used, but this
is essentially the same.

Since there are no built-in functions in the instrument class, this results in a pretty
simple instrument class and lots of info present within the control thread (here).
It might be better to have specific classes inherit from the main instrument class
and then they can have specifi operations. eg a class Attenuator with a function
to set its own attenuation. 
"""

import stuff
import csv
import time
import wx
import numpy as np
import instrument
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

        self.VarV_col, self.Phase_col, self.Atten_col, self.MeasRef_col, self.AutoPhase_col, self.Reserve_col, self.Freq_col,\
        self.VoltRatio_col, self.lcin_range_col, self.meter_range_col, self.nordgs_col = param[8]
        #columns to print to: (Yes a lot of columns, but they can be fiddled with individually now?)
        self.time_print = 12
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

        self.header_row = 5
        
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
        Should force the make safe commands down the GPIB and then quit? Is it even necessary?
        """
        pass

    def com(self, command,send_item=None):
        """Similar to the refstep com. All commands pass here in the form:
        (instrument.function, arguments) and it operates instrument.function(arguments).
        The instrument class always returns a 3 element array:
        (sucess status[True/Falce], readings value, report string).
        Sucess is true when the command was safely sent/recieved (at least visa thinks so).
        Reading is empty unless the instrumetn was read. Report string is to be printed
        to the log file and to the screen stating a breakdown of the
        command/results read+time signature.
        """
        if not self._want_abort:
            if send_item != None:
                sucess,val,string = command(send_item)
                self.PrintSave(string)
                if sucess == False:
                    self._want_abort = 1
                return val
            else:
                sucess,val,string = command()
                self.PrintSave(string)
                if sucess == False:
                    self._want_abort = 1
                return val
        else:
            return 0

    def set_attenuation(self, row):
        """
        Attenuation is set here, the source is set to output off before setting changing
        attenuation.
        """
        self.com(self.source.outpt_off)
        
        case = self.read_grid_cell(row, self.Atten_col)
        
        self.atten.set_atten(case)

        self.com(self.source.outpt_on)
        
    def set_voltage_phase(self, row):
        """
        Function to set the voltage
        """
        if not self._want_abort:
            freq = self.read_grid_cell(row,self.Freq_col)
            self.com(self.source.set_freq,freq)
            #This next one sends none at the moment, no idea what I put it in here for. Does the CH need to even know the attenuation?
            #self.com(self.source.set_value,self.command(row, self.Atten_col))#but this one wont have the correct header...
            volt = self.read_grid_cell(row, self.VarV_col)
            self.com(self.source.set_voltage,volt)
            phase = self.read_grid_cell(row, self.Phase_col)
            self.com(self.source.set_phase,phase)

    def run_swerl(self, row):
        """
        start the swerlein algorithm, perhaps seperate thread?
        """
        case = self.read_grid_cell(row, self.MeasRef_col)
        try:
            case = int(float(case))
        except ValueError:
            self.PrintSave("Could not read row {} reference volt case".format(row))
            return
        
        if case ==1 and not self._want_abort:
            #conditions on when to run swerlein, if there is anything in the box
            #and ofcourse if the algorithm is happy to keep running.
            self.PrintSave("Running GOD's AC at port {}".format(self.meter.adress))
            self.swerl = Swerlein.Algorithm(self.inst_bus, port = self.meter.adress) #sets the thread running.
            loop = True
            while loop == True:
                if self.swerl.ready == True:
                    #loop ends here and function returns the acdcrms readings
                    acdcrms = self.swerl.All_data[0][2]
                    self.set_grid_val(row,self.ref_v_print,acdcrms)
                    loop = False
                elif self.swerl.error == True:
                    #self._want_abort = 1
                    self.PrintSave("Swerlein algorithm failed, NOT aborting")
                    loop = False
                if self._want_abort:
                    loop = False
        
    def set_grid_val(self,row,col,data):
        wx.CallAfter(self.grid.SetCellValue, row, col, str(data))
        
    def read_grid_cell(self,row,col):
        if not self._want_abort:
            value = self.grid.GetCellValue(row, col)
            return value
        else: return 0

    def set_up_lcin(self, row):
        """
        read the reserve and range cells, and send with appropriate packaging
        """
        if not self._want_abort:
            reserve = self.read_grid_cell(row,self.Reserve_col)
            self.com(self.lcin.set_reserve, reserve)
            ran = self.read_grid_cell(row,self.lcin_range_col)
            self.lcin.set_range(ran)
            case = self.read_grid_cell(row,self.AutoPhase_col)
            if case == "1":
                self.com(self.lcin.auto_phase)

    def command(self, row, col):
        """
        NOT USED, BUT THE TWO REFERENCES TO THIS FUNCTION HAVENT
        BEEN REPLACED BY ANYTHING ELSE, NOT SURE IF THEY ARE NECESSARY?

        given a row and column, it will return the full command to send the instrument.
        The command has the column header decorating the actual value, value replaces "$".
        """
        raise Exception
    
        val = str(self.read_grid_cell(row, col))
        com = str(self.read_grid_cell(self.header_row, col)) #reads column headers
        command = com.replace("$",val)
        return command


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

        self.PrintSave('')
        self.com(self.meter.query_error)
        self.PrintSave('meter ESR = '+str(self.com(self.meter.read_instrument)))
        self.com(self.source.query_error)
        self.PrintSave('source ESR = '+str(self.com(self.source.read_instrument)))
        self.com(self.lcin.query_error)
        self.PrintSave('lockin ESR = '+str(self.com(self.lcin.read_instrument)))
        self.PrintSave('')

        ######################END of INITIALISATION##########################

        ######################MEASUREMENT PROCESS############################

        for row in range(self.start_row, self.stop_row + 1):
            if self._want_abort:
                break
            #read all the values in the line.

            self.PrintSave("Spread sheet row "+str(int(row)+1))
            wx.CallAfter(self.grid.SelectRow, row)
            wx.CallAfter(self.grid.ForceRefresh)
            wx.CallAfter(self.grid.Update)

            self.set_attenuation(row)
            self.set_voltage_phase(row)
            self.com(self.source.MeasureSetup)
            self.com(self.lcin.MeasureSetup)
            self.com(self.atten.MeasureSetup)
            self.run_swerl(row)
            self.com(self.meter.MeasureSetup)
            
            nordgs = self.read_grid_cell(row, self.nordgs_col) #number of readings
            try:
                nordgs = int(float(nordgs))
            except TypeError:
                self._want_abort = 1
                nordgs = 1 #so it dosent loop, but still needs an integer to play with
                #could also put an if statement around the for-loop
                
            self.set_up_lcin(row)
            self.com(self.source.MeasureSetup)
            self.com(self.lcin.MeasureSetup)
            #arrays for readings of x,y and theta.
            #theta used to verify the correct reading order of x and y?
            #lockin aparantly switches the order of (x,y) randomly.
            #perhaps solved by clearing the instrument bus?
            #I still havent had such problems.
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
                time.sleep(1)
                tripple_reading = str(self.com(self.lcin.read_instrument))
                #Thre real instrument returns something like "0.1,0.0,0", three readings with commas.
                #If simulated visa is used, only one random float is returned.
                try:
                    x, y, t = tripple_reading.split(",") #For the actual instrument case.
                    #this line is only used for testing with the virtual visa:
                    #x,y,t = [tripple_reading,tripple_reading,tripple_reading]#For the simulated case.
                    self.data.add_multiple([x,y,t]) #Save data triplet into the data list object.
                except ValueError:
                    self.PrintSave("could not unpack tripple reading: {}, aborting".format(tripple_reading))
                    self._want_abort = 1
                    
                if self._want_abort:
                    #break the loop if it wants to abort, speed up aborting process
                    break
                
                x_readings.append(float(x))
                y_readings.append(float(y))
                t_readings.append(float(t))
            #printing res_mod twice?
            printing_cols = [self.sr_range_print,self.sr_res_mod_print,self.time_const_print,self.sr_auto_phas_print]
            #This is the post reading extra-readings.
            #They can be part of the status comand, but that is not the correct repurposing.
            #would only work because the instrument is capable of returning a list,
            #This may not always be the case
            self.com(self.lcin.post_msmnt_query)
            post_msmnt_results = []
            for col in printing_cols:
                reading = str(self.com(self.lcin.read_instrument))
                self.set_grid_val(row, col, reading)
                post_msmnt_results.append(reading)
            
            #the readings would be empty arrays if the program is sent to abort
            #so initialise the values of avg and std as strings 'failed'
            #then if lengths of the arrays are longer than 0, we can compute
            #and therefore save reasonable (calculatable) numbers
            x_avg,x_std,y_avg,y_std,t_avg,t_std = ['failed']*6 #initialise as strings
            if len(x_readings)>0: #If readings are present...
                x_avg = np.average(x_readings)
                x_std = np.std(x_readings)
            if len(y_readings)>0:
                y_avg = np.average(y_readings)
                y_std = np.std(y_readings)
            if len(x_readings)>0:
                t_avg = np.average(t_readings)
                t_std = np.std(t_readings)
                
            self.set_grid_val(row,self.time_print,time.strftime("%Y/%m/%d/ %H:%M:%S", time.localtime()))
            self.set_grid_val(row,self.sr_x_print,x_avg)
            self.set_grid_val(row,self.sr_x_print+1,x_std)
            self.set_grid_val(row,self.sr_y_print,y_avg)
            self.set_grid_val(row,self.sr_y_print+1,y_std)
            self.set_grid_val(row,self.sr_theta_print,"{},{}".format(t_avg,t_std))
            #unused columns?
            # self.sr_range_print = 19
            # self.time_const_print = 20

            #save a line to the excel fiel
            line = [time.strftime("%Y.%m.%d.%H.%M.%S, ", time.localtime())]
            line = line + [x_avg,x_std,y_avg,y_std,"{},{}".format(t_avg,t_std)]
            line = line + post_msmnt_results
            self.sh.append(line)
        self.wb.save(filename = str(self.raw_file_name+'.xlsx'))
        wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, 'GPIB ended'))

        ####################### END of MEASUREMENT PROCESS #####################

