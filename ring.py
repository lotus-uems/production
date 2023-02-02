import math

from . import DB_production as DB
from . import production
    
class RingProduction(production.Production):
    
    def __init__(self, D_in, D, Th, steel, parts, lotus=0):
        self.name = 'Кольцо'
        self.D_in = D_in
        self.D = D
        self.Th = Th
        self.parts = parts
        self.noise_koef = 1
        
        self.DB = DB
        
        self.elements = []
        self.elements_hours = []
        
        # L кромок
        self.L = ((self.D - self.D_in) * self.parts * 2) / 1000
        
        # Считаем площадь
        self.S = (math.pi * (self.D / 1000) ** 2) - (math.pi * (self.D_in / 1000) ** 2)
        self.S_full = (((self.D / 1000) * math.pi) + ((self.D_in / 1000) * math.pi)) + self.L
        
        if lotus == 1:
            self.noise_koef = 1.02            
            
        # Определяем категорию стали
        self.steel_idx = self.DB.steel_category[steel]
    
 
    def calc_hours(self):
        
        self.hours = {}
        
        # 1. Подготовка места 
        self.hours[1] = ['preparation', 0.94]
        
        # 2. Выложить карту, проверить геометрию
        self.hours[2] = ['check_geometry', 0.25]
        
        # 3. Очистка поверхности развертки
        self.hours[3] = ['cleaning_surface', self.S * 0.036 * 2]
        
        # 4. Разметка
        self.hours[4] = ['markup', 0.26]
        
        # 5. Зачистка под контроль кромок 
        self.hours[5] = ['edge_control_cleaning', self.L * 0.06 + (self.Th / 1000) * self.L * 4]
        
        # 6. Обезжиривание 
        self.hours[6] = ['degreasing', self.L * 0.0375]
        
        # 7. Сборка стыка+скобы, клинья (сборка, приварка, срезка) 
        current_assembly_thickness_factor = self.get_coef(self.DB.assembly_thickness_factor, self.Th)
        self.hours[7] = ['assembly', current_assembly_thickness_factor * 4 * 1.2 + 1.5 + 0.2 * self.parts]
        
        # 8. Прихватка стыка+зачистка
        self.hours[8] = ['seam_tack_cleaning', self.hours[7][1] / 2]
        
        # 9. Сварка стыка 
        self.hours[9] = ['welding', (self.L / 2) * self.DB.welding_af[self.Th]]
        
        # 10. Зачистка (Корень, после каждого прохода, снятие усиления)
        self.hours[10] = ['clearing', 1.62 * (self.L / 2)]
        
        # 11. Зачистка под контроли 
        self.hours[11] = ['cleanup_under_control', 0.4 * self.L / 2]
        
        # 12. Подогрев (для обечаек ХМ)
        self.hours[12] = ['heat', 0]
        if self.steel_idx == 3:
            self.hours[12] = ['heat', 0.6]
        
        # 13. Укрытие материалом ( для обечаек ХМ и нерж)
        self.hours[13] = ['cover_meterial', 0]
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[13] = ['cover_meterial', 1]
        
        # 14. Правка
        self.hours[14] = ['pravka_many_parts', 0.25 * self.parts]

        # Заготовка
        # 15 Правка
        self.hours[15] = ['zagotovka_edit', self.get_pravka_interpolated()]
        # 16 Обход листа
        self.hours[16] = ['zagotovka_tеraverse', self.S_full * 0.019]
        # 17 Резка на ЧПУ
        self.hours[17] = ['zagotovka_cut', self.S_full * 0.09]
        # Если нерж или ХМ коэф = 1.2
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[17][1] *= 1.2
            
        # 18 Роспуск отходов
        self.hours[18] = ['zagotovka_waste_disposal', self.S_full * 0.012]
        # 19 Разборка деталей 
        self.hours[19] = ['zagotovka_disassembly_parts', (self.S * (self.Th / 1000) * 7850) * 0.004 * 0.01]
        # 20 Комплектация
        self.hours[20] = ['zagotovka_equipment', (self.S * (self.Th / 1000) * 7850) * 0.006 * 0.01]
        # 21 Маркировка
        self.hours[21] = ['zagotovka_marking', 0.05]
        # 22 Правка на прессе 
        self.hours[22] = ['zagotovka_press_correction', self.get_pravka_interpolated() / 2]
        
        # Механическая обработка 
        # 23 Обработка продольных кромок
        self.hours[23] = ['mechanical_edge_processing', self.L * 0.625]
        
        # 24 Обработка кольцевых стыков
        self.hours[24] = ['mechanical_ring_joint_processing', ((self.D / 1000) * math.pi + (self.D_in / 1000) * math.pi) * self.Th * 0.0072]
        # Если черновая = 0.8
        if self.steel_idx == 1:
            self.hours[24][1] *= 0.8
                       
        # Корректировка по материалам
        if self.steel_idx == 2: # Нерж
            self.set_hours('edge_control_cleaning', self.get_hours('edge_control_cleaning') * 1.2)
            self.set_hours('seam_tack_cleaning', self.get_hours('seam_tack_cleaning') * 1.2)
            self.set_hours('welding', self.get_hours('welding') * 1.2)
            self.set_hours('clearing', self.get_hours('clearing') * 1.2)
            self.set_hours('cleanup_under_control', self.get_hours('cleanup_under_control') * 1.2)
            
        if self.steel_idx == 3: # ХМ
            self.set_hours('seam_tack_cleaning', self.get_hours('seam_tack_cleaning') * 1.3)
            self.set_hours('welding', self.get_hours('welding') * 1.3)
            self.set_hours('clearing', self.get_hours('clearing') * 1.3)
        
        
        # ИТОГ
        self.total_hours = sum([i[1] for i in self.hours.values()])
        
        
    def get_pravka_interpolated(self):
        #print(self.S, self.Th)
        try:
            i_prev = 0
            for i in sorted(self.DB.pravka.keys()):
                if i > self.S:
                    k_prev = 0
                    for k in sorted(self.DB.pravka[i_prev].keys()):
                        if k > self.Th:
                            break
                        k_prev = k
                    break
                i_prev = i
            k_prev_v = self.DB.pravka[i_prev][k_prev]
            k_v = DB.pravka[i][k]
            return (k_prev_v + k_v) / 2
        except:
            return 0.8
