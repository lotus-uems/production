import math

from . import DB_production as DB
from . import production
    
class ShellProduction(production.Production):
    
    def __init__(self, D, H, Th, steel, parts, lotus=0):
        self.name = 'Обечайка'
        self.D = D
        self.Th = Th
        self.H = H
        self.parts = parts
        self.noise_koef = 1
        
        self.DB = DB
        
        self.elements = []
        self.elements_hours = []
        
        # Считаем площадь
        self.S = ((self.D / 1000) * math.pi * (self.H / 1000))
        
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
        self.hours[3] = ['cleaning_surface', ((self.H * self.D * math.pi) * 2 / 1000000) * 0.036]
        
        # 4. Вальцовка (подготовка и вальцовка) 
        current_rolling_thickness_factor = self.get_coef(self.DB.rolling_thickness_factor, self.Th)
        current_rolling_H_factor = self.get_coef(self.DB.rolling_H_factor, self.H)
        current_rolling_base_rate = self.get_coef(self.DB.rolling_base_rates, self.D)
        rollign_koef = current_rolling_thickness_factor * current_rolling_H_factor * current_rolling_base_rate
        self.hours[4] = ['rolling', rollign_koef * 1.2 * 1.2 * 1.6 * 2 + 0.1]
        
        
        # 5. Зачистка под контроль кромок 
        self.hours[5] = ['edge_control_cleaning', ((((self.D * math.pi * 4) + (self.H * 4)) * 60 + (self.Th * (self.D * math.pi * 2 + self.H * 2))) / 1000000) * 4]
        
        # 6. Обезжиривание 
        self.hours[6] = ['degreasing', (((self.Th + 40) * self.H * 2) / 1000000) * 2.4]
        
        # 7. Сборка стыка+скобы, клинья (сборка, приварка, срезка) 
        current_assembly_thickness_factor = self.get_coef(self.DB.assembly_thickness_factor, self.Th)
        current_assembly_altitude_factor = self.get_coef(self.DB.assembly_altitude_factor, self.H)
        self.hours[7] = ['assembly', 4 * self.DB.assembly_base_rate * current_assembly_thickness_factor * current_assembly_altitude_factor]
        
        # 8. Прихватка стыка+зачистка
        self.hours[8] = ['seam_tack_cleaning', self.hours[7][1] / 2]
        
        # 9. Сварка стыка 
        self.hours[9] = ['welding', (self.H / 1000) * self.DB.welding_af[self.Th] * 0.175 * 1.1 * 1.11]
        
        # 10. Зачистка (Корень, после каждого прохода, снятие усиления)
        self.hours[10] = ['clearing', 1.62 * (self.H / 1000)]

        # 11. Калибровка
        self.hours[11] = ['calibration', self.hours[4][1]]
        
        # 12. Зачистка под контроли 
        self.hours[12] = ['cleanup_under_control', 0.4 * (self.H / 1000)]
        
        # 13. Выведение овальности
        self.hours[13] = ['ovality', self.DB.ovality_base_rate * self.find_neighbours(self.DB.ovality_D_factor, self.D)[0][1] * 2]
        #print(self.find_neighbours(self.DB.ovality_D_factor, self.D))
        
        # 14. Подогрев (для обечаек ХМ)
        self.hours[14] = ['heat', 0]
        if self.steel_idx == 3:
            self.hours[14] = ['heat', 0.6]
        
        # 15. Укрытие материалом ( для обечаек ХМ и нерж)
        self.hours[15] = ['cover_meterial', 0]
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[15] = ['cover_meterial', 1]
        
        # 16. Правка (для 2 частей)
        self.hours[16] = ['pravka_many_parts', 0]
        if self.parts > 1:
            self.hours[16] = ['pravka_many_parts', 3.4]

        # 17. Заготовка
        # 17.1 Правка
        self.hours[17] = ['zagotovka_edit', self.get_pravka_interpolated()]
        # 17.2 Обход листа
        self.hours[18] = ['zagotovka_tеraverse', self.S * 0.019]
        # 17.3 Резка на ЧПУ
        self.hours[19] = ['zagotovka_cut', (((self.D/1000)*math.pi)+(self.H/1000))*2*0.09] # Правка от 13.01.2023
        # Если нерж или ХМ коэф = 1.2
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[19][1] *= 1.2
            
        # 17.4 Роспуск отходов
        self.hours[20] = ['zagotovka_waste_disposal', self.S * 0.012]
        # 17.5 Разборка деталей 
        self.hours[21] = ['zagotovka_disassembly_parts', self.S * (self.Th / 1000) * 7850 * 0.004 * 0.01]
        # 17.6 Комплектация
        self.hours[22] = ['zagotovka_equipment', self.S * (self.Th / 1000) * 7850 * 0.006 * 0.01]
        # 17.7 Маркировка
        self.hours[23] = ['zagotovka_marking', 0.05]
        # 17.8 Правка на прессе 
        self.hours[24] = ['zagotovka_press_correction', self.get_pravka_interpolated() * 4] # Правка от 13.01.2023
        
        # 18. Механическая обработка 
        # 18.1 Обработка продольных кромок
        self.hours[25] = ['mechanical_edge_processing', (self.H / 1000) * (self.Th / 1000) * 2 * 10.23 * self.parts] # Правка от 13.01.2023
        
        # 18.2 Обработка кольцевых стыков
        self.hours[26] = ['mechanical_ring_joint_processing', (self.D / 1000) * math.pi * (self.Th / 1000) * 2 * 15.73] # Правка от 13.01.2023
        
        # Если черновая = 0.8
        if self.steel_idx == 1:
            self.hours[26][1] *= 0.8
            
        # Корректировка для нескольких обечаек
        if self.steel_idx == 1: # Черн
            self.hours[5][1] *= self.parts
            self.hours[6][1] *= self.parts
            self.hours[7][1] *= self.parts
            self.hours[8][1] *= self.parts
            self.hours[9][1] *= self.parts
            self.hours[10][1] *= self.parts
            self.hours[12][1] *= self.parts
        if self.steel_idx == 2: # Нерж
            self.hours[4][1] *= 1.2
            self.hours[5][1] *= self.parts * 1.2
            self.hours[6][1] *= self.parts
            self.hours[7][1] *= self.parts
            self.hours[8][1] *= self.parts * 1.2
            self.hours[9][1] *= self.parts * 1.2
            self.hours[10][1] *= self.parts * 1.2
            self.hours[11][1] *= 1.2
            self.hours[12][1] *= self.parts * 1.2
            self.hours[15][1] *= self.parts
        if self.steel_idx == 3: # ХМ
            self.hours[5][1] *= self.parts
            self.hours[6][1] *= self.parts
            self.hours[7][1] *= self.parts
            self.hours[8][1] *= self.parts * 1.3
            self.hours[9][1] *= self.parts * 1.3
            self.hours[10][1] *= self.parts * 1.3
            self.hours[12][1] *= self.parts
            self.hours[15][1] *= 1.5
            self.hours[14][1] *= self.parts
        
        
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
