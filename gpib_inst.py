"""
Organise instruments as classes so that swapping different sources and meters
can be done relatively easily. The objects should return appropriate strings
that can be executed as commands by the try_command method of the GPIBThread
class in gpib_data.py. It assumes that 'self.inst_bus' is used in gpib_data.
"""

import time
class INSTRUMENT(object):
    def __init__(self,inst_bus,letter, **kwargs):
        self.com = {'label':'', 'Ranges':[], 'measure_seperation':'0', 'NoError':'','reset':'','status':'','init':'','MakeSafe':'', 'error':'', 'SettleTime':'0', 'SetValue':'', 'MeasureSetup':'','SingleMsmntSetup':''} #command dictionary
        self.com.update(kwargs) #update dictionary to include all sent commands.
        self.label = self.com["label"]
        self.com.update(label=str(letter)+str(kwargs['label']) )
        self.range = eval(self.com['Ranges'])
        self.bus = self.com['bus']
        #ensure values are ints
        try:
            self.com_settle_time = float(self.com['SettleTime'])
        except:
            print("settle time made into 1, from unreadable: "+str(self.com['SettleTime']))
            self.com_settle_time = 1
        try:
            self.measure_seperation = float(self.com['measure_seperation'])
        except:
            print("measure seperation made into 0, from unreadable: "+str(self.com['measure_seperation']))
            self.measure_seperation = 0

        self.inst_bus = inst_bus #save the instrument bus, either visa or the simulated visa
        

    def create_instrument(self):
        print("creating instruments")
        sucess = False
        string = string = str(time.strftime("%Y.%m.%d.%H.%M.%S, ", time.localtime()))+' Creating '+self.label+': '
        try:
            self.rm = self.inst_bus.ResourceManager()
            self.inst = self.rm.open_resource(self.bus)
            string = string+"sucess"
            sucess = True
        except self.inst_bus.VisaIOError:
            string = string+"visa failed"
        return [sucess,None,string]
    
    def send(self,command):
        sucess = False #did we read sucessfully
        #string to be printed and saved in log file
        string = str(time.strftime("%Y.%m.%d.%H.%M.%S, ", time.localtime()))+' writing to '+self.label+': ' 
        try:
            self.inst.write(command)
            time.sleep(self.com_settle_time)
            string = string+str(command)
            sucess = True
        except self.inst_bus.VisaIOError:
            string = string+"visa failed"
        return [sucess,None,string]
    
    def read_instrument(self):
        val = '0' #value to be returned, string-type like instruments
        sucess = False #did we read sucessfully
        #string to be printed and saved in log file
        string = str(time.strftime("%Y.%m.%d.%H.%M.%S, ", time.localtime()))+' reading '+self.label+': ' 
        try:
            time.sleep(self.measure_seperation)
            val = self.inst.read()
            string = string+str(val)
            sucess = True
        except self.inst_bus.VisaIOError:
            sucess = True #TO BE REMOVED LATER
            string = string+"visa failed"
        return [sucess,val,string]
        
    def set_value(self, value):
        line = str(self.com['SetValue'])
        line = line.replace("$",str(value))
        return self.send(line)

    def initialise_instrument(self):
        return self.send(self.com['init'])

    def make_safe(self):
        return self.send(self.com['MakeSafe'])

    def inst_status(self):
        return self.send(self.com['status'])

    def reset_instrument(self):
        return self.send(self.com['reset'])

    def query_error(self):
        return self.send(self.com['error'])

    def MeasureSetup(self):
        return self.send(self.com['MeasureSetup'])

    def SingleMsmntSetup(self):
        return self.send(self.com['SingleMsmntSetup'])

