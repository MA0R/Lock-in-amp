"""Specific instrument class for the lock in"""
import instrument

class CLARKE_HESS(instrument.INSTRUMENT):
    def __init__(self,inst_bus,adress,label='No label set!'):
        self.label = 'FL'
        self.com_settle_time = 0.1
        self.measure_seperation = 0
        self.adress = adress
        self.inst_bus = inst_bus
        
    def initialise_instrument(self):
        command = 'OUT 0V,50HZ;RANGELCK OFF;PHASESFT ON'
        return self.send(command)

    def make_safe(self):
        command = 'OUT 0V,50HZ;STBY'
        return self.send(command)

    def inst_status(self):
        command = 'RANGE?'
        return self.send(command)

    def reset_instrument(self):
        command = '*RST'
        return self.send(command)

    def query_error(self):
        return self.send('FAULT?')

    def MeasureSetup(self):
        return self.send('OPER')

    def outpt_off(self):
        return self.send('STBY')

    def outpt_on(self):
        return self.send('OPER')

    def set_voltage(self,voltage):
        return self.send('OUT '+str(voltage)+'V')

    def set_phase(self,phase):
        return self.send('PHASE $;PHASESFT ON'.replace('$',phase))

    def set_freq(self,freq):
        return self.send('OUT '+str(phase)+'HZ')

    def set_atten(self,atten):
        return [False,None,'set_atten is not defined yet?']

