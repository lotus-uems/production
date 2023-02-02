import math

from . import production
    
class ScrewProduction(production.Production):
    
    Crew_DB = {
        'М3' : {
            10 : 0.03,
            15 : 0.032,
            20 : 0.033,
            25 : 0.037,
            30 : 0.04,
        },
        'М4' : {
            10 : 0.028,
            15 : 0.032,
            20 : 0.033,
            25 : 0.036,
            30 : 0.039,
            35 : 0.041,
        },
        'М5' : {
            10 : 0.026,
            15 : 0.028,
            20 : 0.031,
            25 : 0.032,
            30 : 0.034,
            35 : 0.036,
            40 : 0.038,
            45 : 0.039,
        },
        'М6' : {
            10 : 0.026,
            15 : 0.029,
            20 : 0.031,
            25 : 0.033,
            30 : 0.035,
            35 : 0.037,
            40 : 0.039,
            45 : 0.04,
            50 : 0.041,
            55 : 0.046,
        },
        'М8' : {
            15 : 0.031,
            20 : 0.031,
            25 : 0.036,
            30 : 0.037,
            35 : 0.038,
            40 : 0.04,
            45 : 0.043,
            50 : 0.046,
            55 : 0.048,
        },
        'М10' : {
            15 : 0.033,
            20 : 0.035,
            25 : 0.038,
            30 : 0.041,
            35 : 0.042,
            40 : 0.043,
            45 : 0.045,
            50 : 0.047,
            55 : 0.049,
            60 : 0.051,
        },
        'М12' : {
            20 : 0.035,
            25 : 0.04,
            30 : 0.042,
            35 : 0.044,
            40 : 0.045,
            45 : 0.048,
            50 : 0.051,
            55 : 0.054,
            60 : 0.057,
            70 : 0.06,
        },
        'М16' : {
            20 : 0.038,
            25 : 0.042,
            30 : 0.044,
            35 : 0.046,
            40 : 0.057,
            45 : 0.056,
            50 : 0.059,
            55 : 0.064,
            60 : 0.068,
            70 : 0.072,
            80 : 0.077,
            90 : 0.098,
            100 : 0.103,
        },
        'М20' : {
            35 : 0.06,
            40 : 0.065,
            45 : 0.07,
            50 : 0.077,
            55 : 0.081,
            60 : 0.086,
            70 : 0.092,
            80 : 0.098,
            90 : 0.103,
            100 : 0.109,
        },
    }
    
    def __init__(self, carving, length, lotus=0):
        self.name = 'Винт'
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
        for i in sorted(self.Crew_DB.keys()):
            if i == self.carving:
                for k in sorted(self.Crew_DB[i].keys()):
                    if k == self.length:
                        return self.Crew_DB[i][k]
        return False