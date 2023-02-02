import math

import STHE.Production.DB_production as DB
from .production import *
from .shell import *
from .ring import *
    
class SupportVerticalProduction(Production):
    
    def __init__(self, D, H_celind, windows, ribs_on_rings, covers, mass_internal, Th, steel, D_ring, D_in_ring, ring_parts, ring_Th, lotus=0):
        self.name = 'Опора вертикальная'
        self.D = D
        self.H_celind = H_celind
        self.Th = Th
        self.steel = steel
        self.windows = windows # [1000, 465]
        self.ribs_on_rings = ribs_on_rings
        self.covers = covers
        self.mass_internal = mass_internal
        self.D_ring = D_ring
        self.D_in_ring = D_in_ring
        self.ring_parts = ring_parts
        self.ring_Th = ring_Th
        
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
        
        B4 = self.Th
        B6 = self.D
        B8 = self.H_celind
        B5 = int(B8 / 2000) + 1
        B7 = B8 / B5
        B9 = len(self.windows)
        B16 = self.ribs_on_rings
        B17 = self.covers
        B18 = self.mass_internal
        
        #print('B5', B5)
        #print('B9', B9, self.windows)
        
        # 1. Подготовка места 
        self.hours[1] = ['preparation', 1.0]
        
        # 2. Выложить карту, проверить геометрию
        self.hours[2] = ['check_geometry', 1.5]
        
        # 3. Разметка главных осей
        self.hours[3] = ['main_axes_marking', 0.55 * (B5 + len(self.windows) + 2)]
        
        # 4. Зачистка кромок +Обезжиривание
        s = 0
        for i in self.windows:
            s += (((i / 1000) * math.pi * (0.04 + B4 / 1000)))
        self.hours[4] = ['edge_cleaning_degreasing', ((((B6 / 1000) * math.pi * (0.04 + B4 / 1000)) * 2) + (0.3 * B16 * (0.04 + B4 / 1000)) + ((B6 + B4 + B4) / 1000) * math.pi * (0.04 + B4 / 1000) + s + (B17 * 1 * (0.04 + B4 / 1000))) * 2.15 * 1.5]
        
        #5. Сборка и сварка технологических деталей
        self.hours[5] = ['assembly_welding_technological_parts', 2.6 * B5]
        
        #6. Сборка кольцевого стыка 
        ring_joint_assembly = self.get_ring_joint_assembly()
        #print('ring_joint_assembly', ring_joint_assembly)
        self.hours[6] = ['assembly_ring_joint', (((ring_joint_assembly * 2 * 1.3) + (0.25 * B5)) * 2 * 1.5) + 5 + 12 + 1.1 + 12 + 1]
        
        #7. Сварка кольцевого стыка 
        self.hours[7] = ['welding_ring_joint', (B6 / 1000 * math.pi) * self.DB.welding_af[self.Th] * 0.175 * 1.1 * 2]
        
        #8. Зачистка (Корень, шов) 
        self.hours[8] = ['clearing_root_seam', 0.75 * (B6 / 1000 * math.pi)]
        
        # 9. Зачистка под контроли 
        self.hours[9] = ['cleanup_under_control', 0.4 * (B6 / 1000 * math.pi)]
        
        # 10. Разметка колец и ребер 
        self.hours[10] = ['marking_rings_ribs', (0.04 * B16 + 0.6) * 2]
        
        # 11. Сборка колец и ребер с обечайками 
        #current_assembly_thickness_factor = self.get_coef(self.DB.assembly_thickness_factor, self.Th)
        #current_assembly_altitude_factor = self.get_coef(self.DB.assembly_altitude_factor, self.D)
        self.hours[11] = ['assembly_rings_ribs_shells', (((ring_joint_assembly * 2 * 1.3) + ((0.25 * (B5 + 2)) + (0.01 * B16))) * 2 * 1.5)]
        
        # 12. Сварка колец и ребер
        self.hours[12] = ['welding_rings_ribs', ((((B6 + B4 + B4) / 1000) * math.pi * 2) + (0.3 * B16 * 2)) * self.DB.welding_madp[self.Th] * 0.55 * 1.2 * 1.2 * 1.2 * 1.2 * 0.8]
        
        # 13. Зачистка шва
        self.hours[13] = ['cleaning_seam', 0.75 * ((((B6 + B4 + B4) / 1000) * math.pi * 2) + (0.3 * B16 * 2))]
        
        # 14. Зачистка под контроли
        self.hours[14] = ['cleanup_under_control', 0.4 * ((((B6 + B4 + B4) / 1000) * math.pi * 2) + (0.3 * B16 * 2))]
        
        # 15. Разметка отверстий
        self.hours[15] = ['hole_marking', 0.14 * B9]
        
        # 16. Сборка и сварка технологических деталей
        self.hours[16] = ['assembly_welding_technological_parts',  5.2 * B9]
        
        # 17. Резка отверстий 
        self.hours[17] = ['hole_cutting', 0.575 * B9]
        
        # 18. Сборка и сварка окон
        s = 0
        for i in self.windows:
            s += (i / 1000) * math.pi * 0.95 * 0.55 * 1.2 * 1.2 * 0.8
            s += (i / 1000) * math.pi * 0.13 + (i / 1000) * math.pi * 0.23
        self.hours[18] = ['assembly_welding_windows', 0.04 * B9 + (0.82 * B9) * 1.75 + s]
    
        # 19. Сборка и сварка накладок, скоб и бобышек 
        self.hours[19] = ['assembly_welding_covers_staples_bosses', (0.08 * B17) + (0.12 * B17) + (1 * 0.95 * 0.55 * 1.2 * 1.2 * 0.8 * B17) + (1 * B17 * 0.23) + 35]
        
        # 20. Сборка и сварка внутренних устройств
        self.hours[20] = ['assembly_welding_internal', 0]
        
        
        # Механическая обработка 
        # 21 Обработка продольных кромок
        self.hours[21] = ['mechanical_height_processing', ((B6 / 1000) * math.pi) * B4 * 0.0072]
        # Если черновая = 0.8
        if self.steel_idx == 1:
            self.hours[21][1] *= 0.8
        
        # ИТОГ
        self.total_hours = sum([i[1] for i in self.hours.values()])
        
        # Расчет обечаек
        shells_hours = 0
        for i in range(int(B5)):
            shell_parts = 1
            if self.D > 2000:
                shell_parts = 2
            shell1 = ShellProduction(self.D, B7, self.Th, self.steel, shell_parts, 0)
            shell1.calc_hours()
            shells_hours += shell1.total_hours
            self.elements.append(shell1)
            #print('Н.Ч. на обечайки: ', shell1.total_hours)
        self.total_hours += shells_hours
        
        # Расчет окон
        shells_hours = 0
        for i in self.windows:
            shell_parts = 1
            shell1 = ShellProduction(i, 1000, self.Th, self.steel, shell_parts, 0)
            shell1.calc_hours()
            shells_hours += shell1.total_hours
            self.elements.append(shell1)
            #print('Н.Ч. на окно: ', shell1.total_hours)
        self.total_hours += shells_hours
        
        # Расчет колец
        rings_hours = 0
        for i in self.windows:
            ring1 = RingProduction(self.D_in_ring, self.D_ring, self.ring_Th, self.steel, self.ring_parts, 0)
            ring1.calc_hours()
            rings_hours += ring1.total_hours
            self.elements.append(ring1)
            #print('Н.Ч. на 1 кольцо: ', ring1.total_hours)
        self.total_hours += rings_hours
        #print('Н.Ч. на все кольца:', rings_hours)
        
        # Норма на ребра
        self.total_hours += 0.6 * self.ribs_on_rings
        
        # Норма на накладки
        self.total_hours += 0.5 * self.covers
        
        # Формируем массив расчетов для всех элементов
        for i in self.elements:
            self.elements_hours.append([i.name, i.hours, i.total_hours])
        
        
    def get_ring_joint_assembly(self):
        try:
            i_prev = 0
            for i in sorted(self.DB.ring_joint_assembly.keys()):
                if i > self.Th:
                    k_prev = 0
                    for k in sorted(self.DB.ring_joint_assembly[i_prev].keys()):
                        if k > self.D:
                            break
                        k_prev = k
                    break
                i_prev = i
            k_prev_v = self.DB.ring_joint_assembly[i_prev][k_prev]
            k_v = DB.ring_joint_assembly[i][k]
            #print(([i_prev, k_prev], [i, k]), self.D)
            return self.interpolation(([i_prev, k_prev_v], [i, k_v]), self.Th)
        except:
            return 0.6
