import math

from . import production
    
class FlangeProduction(production.Production):
    
    MX_DB = {
        19 : 0.69,
        25 : 0.7,
        31 : 0.77,
        37.5 : 0.94,
        50 : 0.97,
        62 : 1.08,
        68 : 1.18,
        81 : 1.27,
        94 : 1.42,
        100 : 1.62,
        125 : 1.69,
        150 : 1.98,
        183 : 2.38,
        205 : 2.77,
        231 : 3.27,
        257 : 3.77,
        283 : 4.05,
        309 : 4.5,
        335 : 5,
        361 : 5.06,
        370 : 5.12,
        380 : 5.32,
        330 : 5.62,
        408 : 5.89,
        458 : 6.4,
        470 : 6.9,
        490 : 7.35,
        511 : 7.7,
        550 : 8,
        580 : 8.3,
    }
    
    KZ_DB = {
        20 : 0.014,
        30 : 0.022,
        40 : 0.03,
        50 : 0.042,
        60 : 0.05,
        75 : 0.064,
        90 : 0.082,
        110 : 0.1,
        130 : 0.12,
        150 : 0.16,
        180 : 0.18,
        210 : 0.24,
        240 : 0.28,
        270 : 0.3,
        300 : 0.34,
        350 : 0.406666667,
        400 : 0.473333333,
    }
    
    def __init__(self, D_in, lotus=0):
        self.name = 'Фланец'
        self.D_in = D_in

        self.noise_koef = 1
        
        self.elements = []
        self.elements_hours = []
        
        if lotus == 1:
            self.noise_koef = 1.02            
            
        
    def calc_hours(self):
        
        self.hours = {}
        
        # 1. Подготовка места 
        self.hours[1] = ['mechanical_fastener_processing', self.MX_DB[self.D_in] + self.find_nearest_KZ() + 0.05 + 0.06 + 0.12 + 0.03]
        
        # ИТОГ
        self.total_hours = sum([i[1] for i in self.hours.values()])
        
    
    def find_nearest_KZ(self):
        for i in self.KZ_DB.keys():
            i_prev = i
            if i > self.D_in:
                return self.KZ_DB[i_prev]
        return False
                