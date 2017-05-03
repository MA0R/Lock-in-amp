"""
Organise instruments as classes so that swapping different sources and meters
can be done relatively easily. The objects should return appropriate strings
that can be executed as commands by the try_command method of the GPIBThread
class in gpib_data.py. It assumes that 'self.inst_bus' is used in gpib_data.
"""
import visa
import time
class INSTRUMENT(object):
    def __init__(self,letter, **kwargs):
        self.com = {'label':'', 'Ranges':[], 'measure_seperation':'0', 'NoError':'','reset':'','status':'','init':'','MakeSafe':'', 'error':'', 'SettleTime':'0', 'SetValue':'', 'MeasureSetup':'','SingleMsmntSetup':''} #command dictionary
        self.com.update(kwargs) #update dictionary to include all sent commands.
        self.label = self.com["label"]
        self.com.update(label=str(letter)+str(kwargs['label']) )
        self.range = eval(self.com['Ranges'])
        #ensure values are ints
        try:
            com_settle_time = float(self.com['SettleTime'])
        except:
            self.com.update({'SettleTime':'1'})
        try:
            self.measure_seperation = float(self.com['measure_seperation'])
        except:
            self.measure_seperation = 0

    def create_instrument(self):
        """
        Run exec on the output string of this method in GPIBThread.run in
        order to establish the instrument in Visa.
        """
        bus = self.com['bus']
        bus = '"'+bus+'"'
        commandstring = "self.rm.open_resource(" +bus + ")'"
        exec1 = "self.try_command('self."+ self.com['label'] + ' = ' + commandstring
        exec2 = ",'Failing to create " + self.com['label'] + "','ex',"+str(self.com['SettleTime'])+")"
        execstring = exec1 + exec2
        return execstring


    def initialise_instrument(self):
        """
        Run exec on the output string of this method in GPIBThread.
        Based off of initialization state given.
        """
        commandstring = 'self.' + self.com['label'] + ".write('" + self.com['init'] +"')"
        execstring = 'self.try_command(' + '"' + commandstring + '"' + ", 'Failing to set initial state of " + self.com['label'] + "', 'ex',"+str(self.com['SettleTime'])+")"
        return execstring

    def make_safe(self):
        """
        Running exec on th eoutput will go through the Make_Safe routine of the instrument,
        Make_Safe should not include a command to reset the instrument unless instrument
        is then set up again either later in the command chain or in the pre measure set up.
        Must include at least: setting DVM range to AUTO or max range, and setting voltage of
        a voltage source to zero and outputs off.
        """
        commandstring = 'self.' + self.com['label'] + ".write('" + self.com['MakeSafe'] +"')"
        execstring = 'self.try_command(' + '"' + commandstring + '"' + ", 'Failing to set initial state of " + self.com['label'] + "', 'ex',"+str(self.com['SettleTime'])+")"
        return commandstring

    def read_instrument(self):
        """
        Run eval on the output string of this method in GPIBThread.
        Simply reads all that is in buffer, or takes current reading.
        """
        #the form of data returned might affect what is done here, i.e. zeroth element of list not always what is wanted
        commandstring = "'"+"self." + self.com['label'] + ".read()"+"'"
        evalstring = 'self.try_command(' + commandstring + ", 'Failing to read " + self.com['label'] + "', 'ev',"+str(self.com['SettleTime'])+")"
        return evalstring

    def inst_status(self):
        """
        Sends command to prepare status string
        """
        commandstring = 'self.' + self.com['label'] + ".write('" + self.com['status'] +"')"
        commandstring = '"' + commandstring + '"'
        execstring = "self.try_command(" + commandstring + ", 'Failing to find " + self.com['label'] + "', 'ex',"+str(self.com['SettleTime'])+")"
        return execstring

    def reset_instrument(self):
        """
        Runs reset as specified by user
        """
        commandstring = 'self.' + self.com['label'] + ".write('" + self.com['reset'] +"')"
        commandstring = '"' + commandstring + '"'
        execstring = "self.try_command(" + commandstring + ", 'Failing to find " + self.com['label'] + "', 'ex',"+str(self.com['SettleTime'])+")"
        return execstring

    def query_error(self):
        """
        Sends instrument command to generate error code, to be read later by read_instrument
        """
        commandstring = 'self.' + self.com['label'] + ".write('" + self.com['error'] +"')"
        commandstring = '"' + commandstring + '"'
        execstring = "self.try_command(" + commandstring + ", 'Failing to query " + self.com['label'] + "', 'ex',"+str(self.com['SettleTime'])+")"
        return execstring

    def set_value(self, value):
        """
        Set some value, normally 'value' is read from the table.
        """
        line = str(self.com['SetValue'])
        line = line.replace("$",str(value))
        commandstring = 'self.' + self.com['label'] + ".write('" + line +  "')"
        commandstring = '"' + commandstring + '"'
        execstring = "self.try_command(" + commandstring + ", 'Failing to set value " + self.com['label'] + "', 'ex',"+str(self.com['SettleTime'])+")"
        return execstring

    def MeasureSetup(self):
        """
        set up for the DVM, might be setting the NPLC or memory format. Specified by user, executed before each measure sequence.
        """
        commandstring = 'self.' + self.com['label'] + ".write('" + self.com['MeasureSetup'] +"')"
        execstring = 'self.try_command(' + '"' + commandstring + '"' + ", 'Failing to set initial state of " + self.com['label'] + "', 'ex',"+str(self.com['SettleTime'])+")"
        return execstring

    def SingleMsmntSetup(self):
        """
        Optional setting up of instrument before individual measurements, for example NPLC can be reset.
        """
        commandstring = 'self.' + self.com['label'] + ".write('" + self.com['SingleMsmntSetup'] +"')"
        execstring = 'self.try_command(' + '"' + commandstring + '"' + ", 'Failing to set initial state of " + self.com['label'] + "', 'ex',"+str(self.com['SettleTime'])+")"
        return execstring

