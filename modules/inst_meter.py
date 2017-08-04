"""Specific instrument class for the meter"""
import instrument

class METER(instrument.INSTRUMENT):
    def __init__(self,inst_bus,adress,label='No label set!'):
        self.label = 'HP'
        self.com_settle_time = 0.1
        self.measure_seperation = 0
        self.adress = adress
        self.inst_bus = inst_bus
        self.no_error = '0\n'
        
    def initialise_instrument(self):
        command = 'END 2; ACV AUTO; AZERO ON;DELAY 0;NPLC 20'
        return self.send(command)

    def make_safe(self):
        command = 'DCV AUTO'
        return self.send(command)

    def inst_status(self):
        command = 'RANGE?'
        return self.send(command)

    def reset_instrument(self):
        command = 'RESET'
        return self.send(command)

    def query_error(self):
        return self.send('ERR?')

    def MeasureSetup(self):
        return self.send('None')

    def SingleMsmntSetup(self):
        return self.send('None')

