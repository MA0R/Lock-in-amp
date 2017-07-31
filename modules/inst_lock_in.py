"""Specific instrument class for the CH"""
import instrument

class LOCK_IN(instrument.INSTRUMENT):
    
    def __init__(self,inst_bus,adress,label='No label set!'):
        self.label = 'SR'
        self.com_settle_time = 0.1
        self.measure_seperation = 0
        self.adress = adress
        self.inst_bus = inst_bus
        
    def initialise_instrument(self):
        command = 'OUTX 1; OVRM 1; OFSL 3; SYNC 1; OFLT 8; FMOD 2\n'
        return self.send(command)

    def make_safe(self):
        command = 'None'
        return self.send(command)

    def inst_status(self):
        return self.send('*ESR?\n')

    def reset_instrument(self):
        command = '*CLS; *ESE\n'
        return self.send(command)

    def query_error(self):
        return self.send('*ESR?\n')

    def MeasureSetup(self):
        return self.send('None')

    def SingleMsmntSetup(self):
        return self.send('REST;PAUS;SNAP? 1,2,4\n')

    def set_reserve(self,reserve):
        command = 'RMOD {}'.format(reserve)
        return self.send(command)

    def set_range(self,ran):
        return self.send('SENS {}'.format(ran))

    def auto_phase(self):
        return self.send('APHS')

    def post_msmnt_query(self):
        return self.send('SENS?;RMOD?;OFLT?;PHAS?\n')

    

