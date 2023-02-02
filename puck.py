import math

from .production import *
    
class PuckProduction(Production):
    
    Puck_DB = {
        'М3' : 0.012,
        'М4' : 0.012,
        'М5' : 0.012,
        'М6' : 0.0128,
        'М8' : 0.0137,
        'М10' : 0.0154,
        'М12' : 0.017,
        'М14' : 0.0188,
        'М16' : 0.0197,
        'М18' : 0.0206,
        'М20' : 0.0222,
        'М22' : 0.025,
        'М24' : 0.03,
        'М27' : 0.036,
        'М30' : 0.047,
        'М36' : 0.059,
        'М42' : 0.073,
        'М48' : 0.084,
    }
    
    def __init__(self, carving, lotus=0):
        self.name = 'Шайба'
        self.carving = carving
        self.noise_koef = 1
        
        self.elements = []
        self.elements_hours = []
        
        if lotus == 1:
            self.noise_koef = 1.02            
            
        
    def calc_hours(self):
        
        self.hours = {}
        
        # 1. Подготовка места 
        self.hours[1] = ['mechanical_fastener_processing', self.Puck_DB[self.carving]]
        
        # ИТОГ
        self.total_hours = sum([i[1] for i in self.hours.values()])
