import math

from . import DB_production as DB
from . import production

from . import flange
from . import nozzle
    
class FittingProduction(production.Production):
    
    def __init__(self, D_in, Th, flange_D_in, nozzle_D_in, nozzle_H, steel, lotus=0):
        self.name = 'Штуцер (фланец + патрубок)'
        self.Th = Th
        self.D_in = D_in
        self.flange_D_in = flange_D_in
        self.nozzle_D_in = nozzle_D_in
        self.nozzle_H = nozzle_H
        
        self.steel = steel
        
        self.elements = []
        self.elements_hours = []
        
        self.noise_koef = 1
        
        self.DB = DB

        if lotus == 1:
            self.noise_koef = 1.02            
            
        # Определяем категорию стали
        self.steel_idx = self.DB.steel_category[steel]
 
    def calc_hours(self):
        
        self.hours = {}
        
        B4 = self.D_in
        B5 = self.Th
        
        # 1. Подготовка места 
        self.hours[1] = ['preparation', 0.2]
        
        # 2. Выложить карту, проверить геометрию
        self.hours[2] = ['check_geometry', 0.2]
        
        # 3. Разметка главных осей
        self.hours[3] = ['main_axes_marking', 0.1]
        
        # 4. Зачистка кромок +Обезжиривание
        self.hours[4] = ['edge_cleaning_degreasing', ((B4 / 1000) * math.pi) * ((B5 / 1000) * 2 + 0.04)]
        
        #5. Сборка и сварка технологических деталей
        if self.D_in >= 200:
            self.hours[5] = ['assembly_welding_technological_parts', 2]
        
        #6. Сборка стыка фланца и патрубка
        assembling_joint_flange_nozzle = self.get_assembling_joint_flange_nozzle()
        self.hours[6] = ['assembling_joint_flange_nozzle', assembling_joint_flange_nozzle * 1.5]
        
        #7. Сварка стыка фланца и патрубка
        welding_flange_nozzle = self.DB.welding_flange_nozzle[self.Th]
        self.hours[7] = ['welding_joint_shell_ribs', (((welding_flange_nozzle * (B4 / 1000) * math.pi) + (0.25 * 2)) * 0.2) + 1 + 4]
        if self.D_in < 200:
            self.hours[7][1] = (((welding_flange_nozzle * (B4 / 1000) * math.pi) + (0.25 * 2)) * 0.2)
        
        #8. Зачистка (Корень, шов)
        self.hours[8] = ['clearing_root_seam', 0.75 * (B4 / 1000 * math.pi)]
        
        #9. Зачистка под контроли 
        self.hours[9] = ['cleanup_under_control', 0.4 * (B4 / 1000 * math.pi)]
        
        # ИТОГ
        self.total_hours = sum([i[1] for i in self.hours.values()])
        
        # Расчет фланца
        flange1 = flange.FlangeProduction(self.flange_D_in, 0)
        flange1.calc_hours()
        self.elements.append(flange1)
        
        # Расчет патрубка
        nozzle1 = nozzle.NozzleProduction(self.nozzle_D_in, self.nozzle_H, 0)
        nozzle1.calc_hours()
        if self.D_in < 200:
            for i in nozzle1.hours.keys():
                nozzle1.hours[i][1] *= 2
            nozzle1.total_hours *= 2
        self.elements.append(nozzle1)
        
        # Формируем массив расчетов для всех элементов
        for i in self.elements:
            self.elements_hours.append([i.name, i.hours, i.total_hours])
        
        
    def get_assembling_joint_flange_nozzle(self):
        try:
            i_prev = 0
            for i in sorted(self.DB.assembling_joint_flange_nozzle.keys()):
                if i > self.Th:
                    k_prev = 0
                    for k in sorted(self.DB.assembling_joint_flange_nozzle[i_prev].keys()):
                        if k > self.D_in:
                            break
                        k_prev = k
                    break
                i_prev = i
            k_prev_v = self.DB.ring_joint_assembly[i_prev][k_prev]
            k_v = DB.ring_joint_assembly[i][k]
            return self.interpolation(([i_prev, k_prev_v], [i, k_v]), self.Th)
        except:
            return 0.6