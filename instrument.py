"""
A general instrument class that returns a status for each command sent
or recieved from its instrument. This allows it to be used with the "com"
function in the main algorithm, when visa fails it does not halt the
whole program but reports the failure instead.
Current commands in this class always send 'None' to the instrument,
which is a default that gets ignored.
"""

import time
class INSTRUMENT(object):
    def __init__(self,inst_bus,adress,label='No label set!'):
        self.label = label
        self.com_settle_time = 0
        self.measure_seperation = 0
        self.adress = adress
        self.inst_bus = inst_bus #save the instrument bus, either visa or the simulated visa
        

    def create_instrument(self):
        """
        Needs to be called prior to any commands being sent or recieved.
        Creates the visa instrument object, to which commands will be sent
        and recieved.
        """
        print("creating instruments")
        sucess = False
        string = string = str(time.strftime("%Y.%m.%d.%H.%M.%S, ", time.localtime()))+' Creating '+self.label+': '
        try:
            self.rm = self.inst_bus.ResourceManager()
            self.inst = self.rm.open_resource(self.adress)
            string = string+"sucess"
            sucess = True
        except self.inst_bus.VisaIOError:
            string = string+"visa failed"
        return [sucess,None,string]
    
    def send(self,command):
        """
        From here a command is sent to the instrument, surrounded by the try block.
        If the command fails, it does not halt the problem but sends back a failed status.
        """
        sucess = False #did we read sucessfully
        #string to be printed and saved in log file
        string = str(time.strftime("%Y.%m.%d.%H.%M.%S, ", time.localtime()))+' writing to '+self.label+': '
        if command in (None,'None','None\n',''):
            return [True,None,string+'"None" specified, command ignored']
        try:
            self.inst.write(command)
            time.sleep(self.com_settle_time)
            string = string+str(command)
            sucess = True
        except self.inst_bus.VisaIOError:
            string = string+"visa failed"
        return [sucess,None,string]
    
    def read_instrument(self):
        """
        Similar to the send function, but reads and expects a return value too.
        """
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

    def initialise_instrument(self):
        return self.send("None")

    def make_safe(self):
        return self.send("None")

    def inst_status(self):
        return self.send("None")

    def reset_instrument(self):
        return self.send("None")

    def query_error(self):
        return self.send("None")

    def MeasureSetup(self):
        return self.send("None")

    def SingleMsmntSetup(self):
        return self.send("None")

