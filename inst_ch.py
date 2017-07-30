"""Specific instrument class for the lock in"""
import instrument

class CLARKE_HESS(instrument.INSTRUMENT):
    def __init__(self,inst_bus,adress,label='No label set!'):
        self.label = 'CH'
        self.com_settle_time = 0.1
        self.measure_seperation = 0
        self.adress = adress
        self.inst_bus = inst_bus
        
    def initialise_instrument(self):
        command = 'R0V0F50P0'
        return self.send(command)

    def make_safe(self):
        command = 'S'
        return self.send(command)

    def inst_status(self):
        command = '*STB?'
        return self.send(command)

    def reset_instrument(self):
        command = '*RST'
        return self.send(command)

    def query_error(self):
        return self.send('*STB?')

    def MeasureSetup(self):
        return self.send('N')

    def outpt_off(self):
        return self.send('S')

    def outpt_on(self):
        return self.send('N')

    def set_voltage(self,voltage):
        return self.send('V'+str(voltage))

    def set_phase(self,phase):
        return self.send('P'+str(phase))

    def set_freq(self,freq):
        return self.send('F'+str(freq))

    def set_atten(self,atten):
        return [False,None,'set_atten is not defined yet?']

