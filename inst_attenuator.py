"""Specific instrument class for the attenuator"""

import instrument

class ATTENUATOR(instrument.INSTRUMENT):
    def __init__(self,inst_bus,adress,label='No label set!'):
        self.label = 'AG'
        self.com_settle_time = 0.1
        self.measure_seperation = 0
        self.adress = adress
        self.inst_bus = inst_bus
        
    def set_atten(self, atten):
        try:
            case = int(float(atten))
        except TypeError:
            return [False,None,'Invalid attenuation {}'.format(atten)]
        if case == 0:
            return self.send("B123\nB567")
        elif case == 20:
            return self.send("A2B13\nB567")
        elif case == 40:
            return self.send("A3B12\nB567")
        elif case == 60:
            return self.send("A23B1\nB567")
        elif case == 80:
            return self.send("A3B12\\A7B56")
        elif case == 100:
            return self.send("A23B1\nA7B56")
        elif case == 120:
            return self.send("A23B1\nA67B5")
        else:
            return [False,None,'Invalid attenuation {}'.format(atten)]
        
    def initialise_instrument(self):
        return self.send("B123\nB567")

    def make_safe(self):
        return self.send("B123\nB567")

    def reset_instrument(self):
        return self.send("B123\nB567")

    
