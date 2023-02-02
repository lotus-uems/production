import math

from .production import *
    
class PinProduction(Production):
    
    Pin_DB = {
        'М12' : {
            '50-60' : 0.13,
            '70-80' : 0.14,
            '90-100' : 0.14,
            '110-120' : 0.16,
            '130-140' : 0.18,
            '150-160' : 0.19,
            '180-200' : 0.2,
            '220-240' : 0.21,
            '260-280' : 0.22,
            '300-320' : 0.23,
            '340-360' : 0.24,
            '380-400' : 0.25,
        },
        'М14' : {
            '50-60' : 0.14,
            '70-80' : 0.14,
            '90-100' : 0.15,
            '110-120' : 0.16,
            '130-140' : 0.19,
            '150-160' : 0.2,
            '180-200' : 0.21,
            '220-240' : 0.22,
            '260-280' : 0.23,
            '300-320' : 0.24,
            '340-360' : 0.25,
            '380-400' : 0.27,
        },
        'М16' : {
            '50-60' : 0.14,
            '70-80' : 0.15,
            '90-100' : 0.16,
            '110-120' : 0.18,
            '130-140' : 0.19,
            '150-160' : 0.2,
            '180-200' : 0.22,
            '220-240' : 0.23,
            '260-280' : 0.24,
            '300-320' : 0.25,
            '340-360' : 0.26,
            '380-400' : 0.28,
        },
        'М20' : {
            '50-60' : 0.15,
            '70-80' : 0.16,
            '90-100' : 0.18,
            '110-120' : 0.19,
            '130-140' : 0.21,
            '150-160' : 0.22,
            '180-200' : 0.23,
            '220-240' : 0.24,
            '260-280' : 0.26,
            '300-320' : 0.27,
            '340-360' : 0.28,
            '380-400' : 0.32,
        },
        'М22' : {
            '70-80' : 0.17,
            '90-100' : 0.18,
            '110-120' : 0.2,
            '130-140' : 0.21,
            '150-160' : 0.22,
            '180-200' : 0.23,
            '220-240' : 0.24,
            '260-280' : 0.27,
            '300-320' : 0.29,
            '340-360' : 0.3,
            '380-400' : 0.34,
        },
        'М24' : {
            '70-80' : 0.18,
            '90-100' : 0.19,
            '110-120' : 0.21,
            '130-140' : 0.21,
            '150-160' : 0.23,
            '180-200' : 0.24,
            '220-240' : 0.27,
            '260-280' : 0.28,
            '300-320' : 0.3,
            '340-360' : 0.31,
            '380-400' : 0.36,
        },
        'М27' : {
            '90-100' : 0.2,
            '110-120' : 0.21,
            '130-140' : 0.22,
            '150-160' : 0.24,
            '180-200' : 0.25,
            '220-240' : 0.26,
            '260-280' : 0.29,
            '300-320' : 0.31,
            '340-360' : 0.32,
            '380-400' : 0.37,
        },
        'М30' : {
            '90-100' : 0.21,
            '110-120' : 0.22,
            '130-140' : 0.23,
            '150-160' : 0.26,
            '180-200' : 0.27,
            '220-240' : 0.28,
            '260-280' : 0.31,
            '300-320' : 0.33,
            '340-360' : 0.35,
            '380-400' : 0.38,
        },
        'М36' : {
            '150-160' : 0.27,
            '180-200' : 0.29,
            '220-240' : 0.3,
            '260-280' : 0.34,
            '300-320' : 0.35,
            '340-360' : 0.38,
            '380-400' : 0.39,
            '450' : 0.42,
            '500' : 0.45,
        },
        'М42' : {
            '150-160' : 0.28,
            '180-200' : 0.3,
            '220-240' : 0.32,
            '260-280' : 0.35,
            '300-320' : 0.37,
            '340-360' : 0.41,
            '380-400' : 0.42,
            '450' : 0.45,
            '500' : 0.49,
        },
        'М48' : {
            '180-200' : 0.31,
            '220-240' : 0.34,
            '260-280' : 0.37,
            '300-320' : 0.4,
            '340-360' : 0.44,
            '380-400' : 0.45,
            '450' : 0.47,
            '500' : 0.51,
        },
        'М56' : {
            '180-200' : 0.32,
            '220-240' : 0.36,
            '260-280' : 0.39,
            '300-320' : 0.43,
            '340-360' : 0.45,
            '380-400' : 0.48,
            '450' : 0.53,
            '500' : 0.55,
            '550' : 0.57,
        },
        'М64' : {
            '220-240' : 0.43,
            '260-280' : 0.42,
            '300-320' : 0.45,
            '340-360' : 0.48,
            '380-400' : 0.53,
            '450' : 0.55,
            '500' : 0.59,
            '550' : 0.6,
        },
    }
    
    def __init__(self, carving, length, lotus=0):
        self.name = 'Шпилька'
        self.carving = carving
        self.length = length
        self.noise_koef = 1
        
        self.elements = []
        self.elements_hours = []
        
        if lotus == 1:
            self.noise_koef = 1.02            
            
        
    def calc_hours(self):
        
        self.hours = {}
        
        # 1. Подготовка места 
        self.hours[1] = ['mechanical_fastener_processing', self.get_from_DB()]
        
        # ИТОГ
        self.total_hours = sum([i[1] for i in self.hours.values()])

        
    def get_from_DB(self):
        for i in sorted(self.Pin_DB.keys()):
            if i == self.carving:
                for k in sorted(self.Pin_DB[i].keys()):
                    if k == self.length:
                        return self.Pin_DB[i][k]
        return False