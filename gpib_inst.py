"""
Organise instruments as classes so that swapping different sources and meters
can be done relatively easily. The objects should return appropriate strings
that can be executed as commands by the try_command method of the GPIBThread
class in gpib_data.py. It assumes that 'self.inst_bus' is used in gpib_data.
"""
import visa
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
            self.com.update({'SettleTime':'1'})
        try:
            self.measure_seperation = float(self.com['measure_seperation'])
        except:
            self.measure_seperation = 0

        self.inst_bus = inst_bus #save the instrument bus, either visa or the simulated visa
        

    def create_instrument(self):
        try:
            self.rm = self.inst_bus.ResourceManager()
            self.inst = self.rm.open_resource(self.bus)
            
        except self.inst_bus.VisaIOError:
            pass
        
    def send(self,command):
        state = 'ok'
        try:
            self.inst.write(command)
            time.sleep(self.com_settle_time)
        except self.inst_bus.VisaIOError:
            state = 'fail'
        return state
    
    def read_instrument(self):
        val = 'fail'
        try:
            time.sleep(self.measure_seperation)
            val = self.inst.read()
        except self.inst_bus.VisaIOError:
            pass
        return val
        
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

