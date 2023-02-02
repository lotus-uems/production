import math

from . import DB_production as DB
from . import production
    
class BottomSphericalProduction(production.Production):
    
    def __init__(self, D, Th, steel, petals, lotus=0):
        self.name = 'Днище (сферическое)'
        self.Th = Th
        self.petals = petals
        self.D = D
        self.noise_koef = 1
        
        self.DB = DB
        
        self.elements = []
        self.elements_hours = []
        
        B5 = self.Th
        B6 = self.petals
        B7 = self.D
        
        # Считаем площадь
        self.Szag = (((((B7 / 1000) * math.pi) / 6) + 0.3) + ((((B7 / 1000) * math.pi) / (2 * B6)) + 0.3)) + (((((((B7 / 1000) * math.pi) / 6) + 0.3) + ((((B7 / 1000) * math.pi)/(2 * B6)) + 0.3))/2) + 0.6) * 2
        self.S = ((((((B7 / 1000) * math.pi) / 6) + 0.3) + ((((B7 / 1000) * math.pi) / (2 * B6)) + 0.3)) / 2) * math.sqrt(((((((((B7 / 1000) * math.pi) / 6) + 0.3) + ((((B7 / 1000) * math.pi) / (2 * B6)) + 0.3)) / 2) + 0.6) ** 2) - ((((((B7 / 1000) * math.pi) / 6) + 0.3) - ((((B7 / 1000) * math.pi) / (2 * B6)) + 0.3)) ** 2))
        
        if lotus == 1:
            self.noise_koef = 1.02 
            
        # Определяем категорию стали
        self.steel_idx = self.DB.steel_category[steel]
            
 
    def calc_hours(self):
        
        B5 = self.Th
        B6 = self.petals
        B7 = self.D
        C7 = self.Szag
        D7 = self.S
        
        self.hours = {}
        
        # 1. Подготовка места 
        self.hours[1] = ['preparation', 0.94]
        
        # 2. Выложить карту, проверить геометрию
        self.hours[2] = ['check_geometry', 1.5]
        
        # 3. Очистка поверхности развертки
        self.hours[3] = ['cleaning_surface', D7 * 0.036 * B6 * 1.5]
        
        #4 Штамповка (ШТ)
        self.hours[4] = ['stamping', ((((B5 * 1.5) / 60) * 3) + (0.7 * 3) + 0.92 + 2 + (0.48 * 2) + (((B5 * 1.5) / 60) * 3 * 0.8)) * 1.5 * B6]
        
        # 5. Сборка, сварка строповочных элементов
        self.hours[5] = ['assembly_and_welding_of_rigging_elements', 1.5 * B6]
        
        # 6. Разметка, срезка припуска, доводка фасок
        chamfering = self.get_coef(self.DB.chamfering, self.Th)
        self.hours[6] = ['cutting_allowances', ((0.08 * 2) + (0.01 * round((C7 / 0.5), 0)) + (2 * 4 * 0.345) + ((chamfering * C7) * 2 * 2)) * B6]
        
        # 7. Зачистка под контроль кромок 
        self.hours[7] = ['edge_control_cleaning', (((C7 * (100 + B5) * B6) + (100 * B5 * ((B7 / 2) * math.pi))) / 1000000)]
        
        # 8. Обезжиривание 
        self.hours[8] = ['degreasing', (((C7 * 20 * 4) + (B5 * B7 * 2)) / 1000000) * 2.4 * 2]
        
        # 9. Сборка стыков лепестков (скобы, клинья, сборка, приварка, срезка)
        current_assembly_thickness_factor = self.get_coef(self.DB.assembly_thickness_factor, self.Th)
        current_assembly_diametr_factor = self.get_coef(self.DB.assembly_altitude_factor, self.D)
        self.hours[9] = ['assembly_of_petal_joints', 2 * self.DB.assembly_base_rate * current_assembly_thickness_factor * current_assembly_diametr_factor * 1.3 + 3.2]
        
        # 10. Прихватка стыка+зачистка
        self.hours[10] = ['seam_tack_cleaning', self.hours[8][1] / 2]
        
        # 11. Сварка стыков лепестков
        self.hours[11] = ['welding_petals', (((((((B7 / 1000) * math.pi) / 6) + 0.3) + ((((B7 / 1000) * math.pi) / (2 * B6)) + 0.3)) / 2) + 0.6) * self.DB.welding_madp[self.Th] * B6 * 1.5 * 0.55 * 1.2 * 4 * 0.8]
                          
        #12. Зачистка (Корень, после каждого прохода, снятие усиления)
        self.hours[12] = ['clearing', (1.03 * (((((((B7 / 1000) * math.pi) / 6) + 0.3) + ((((B7 / 1000) * math.pi) / (2 * B6)) + 0.3)) / 2) + 0.6) * 6) + (0.6 * (((((((B7 / 1000) * math.pi) / 6) + 0.3) + ((((B7 / 1000) * math.pi) / (2 * B6)) + 0.3)) / 2) + 0.6) * 6) + (1.7 * (((((((B7 / 1000) * math.pi) / 6) + 0.3) + ((((B7 / 1000) * math.pi) / (2 * B6)) + 0.3)) / 2) + 0.6) * 6) + (0.48 * (((((((B7 / 1000) * math.pi) / 6) + 0.3) + ((((B7 / 1000) * math.pi) / (2 * B6)) + 0.3)) / 2) + 0.6) * 6) + (1.9 * (((((((B7 / 1000) * math.pi) / 6) + 0.3) + ((((B7 / 1000) * math.pi) / (2 * B6)) + 0.3)) / 2) + 0.6) * 6)]
        
        # 13. Зачистка под контроли 
        self.hours[13] = ['cleanup_under_control', 0.4 * (((B7 / 1000) / 2) * math.pi)]
        
        #14. Сборка стыка крышки и лепестков (скобы, клинья, сборка, приварка, срезка)
        current_assembly_thickness_factor = self.get_coef(self.DB.assembly_thickness_factor, self.Th)
        current_assembly_diametr_factor = self.get_coef(self.DB.assembly_altitude_factor, self.D)
        self.hours[14] = ['assembly_of_the_lid_and_petals', ((current_assembly_thickness_factor * current_assembly_diametr_factor * 2) * 1.3 + 3.2) * 2]
        
        #15. Разметка, срезка припуска, доводка фасок
        self.hours[15] = ['cutting_allowances', 0.1 + 0.21 * (((B7 / 1000) / 2) * math.pi) * 1.5]
    
        #16. Прихватка стыка + зачистка
        self.hours[16] = ['seam_tack_cleaning', self.hours[14][1] / 2]
        
        #17. Сварка стыка крышки и лепестков
        self.hours[17] = ['welding_lid_and_petals', 1 + 2 + (((B7 / 1000) / 2) * math.pi) * self.DB.welding_madp[self.Th]]
        
        #18. Зачистка (Корень, после каждого прохода, снятие усиления)
        self.hours[18] = ['clearing', (1.03 * (((B7 / 1000) / 2) * math.pi)) + (0.6 * (((B7 / 1000) / 2) * math.pi)) + (1.7 * (((B7 / 1000) / 2) * math.pi)) + (0.48 * (((B7 / 1000) / 2) * math.pi)) + (1.9 * (((B7 / 1000) / 2) * math.pi))]
                          
        #19. Зачистка под контроли 
        self.hours[19] = ['cleanup_under_control', 0.4 * (((B7 / 1000) / 2) * math.pi)]
        
        #20. Технологичческие детали
        self.hours[20] = ['technological_components', 15]
        
        #21. Обрезка борта
        self.hours[21] = ['cut_border', (0.085 * (B7 / 1000) * math.pi) * 1.2 + 0.39 + 0.06 * ((B7 / 1000) * math.pi)]
        
        #22. Подогрев (для обечаек ХМ)
        self.hours[22] = ['heat', 0]
        if self.steel_idx == 3:
            self.hours[22][1] = 3
        
        #23. Укрытие материалом ( для обечаек ХМ и нерж)
        self.hours[23] = ['cover_meterial', 0]
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[23][1] = 5
        
        #24. Сборка, сварка и срезка тех. деталей для штамповки (КЗ)
        self.hours[24] = ['assembly_for_stamping', 12.45]
        
    
        # ХМ и нерж.
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[5][1] *= 1.3
            self.hours[10][1] *= 1.3
            self.hours[11][1] *= 1.3
            self.hours[12][1] *= 1.3
            self.hours[16][1] *= 1.3
            self.hours[17][1] *= 1.3
            self.hours[18][1] *= 1.3
            
            
        # Заготовка
        # 25. Правка
        self.hours[25] = ['zagotovka_edit', (B6 + 1) * self.get_pravka_interpolated()]
        # 26. Защита от окалины
        self.hours[26] = ['zagotovka_guard', (0.35 * C7 * (0.04 * 2 + (B5 / 1000))) * B6]
        # 27. Обход листа
        self.hours[27] = ['zagotovka_tеraverse', 0.3 * (B6 + 1)]
        # 28. Резка на ЧПУ
        self.hours[28] = ['zagotovka_cut', ((C7 * 0.095 * B6) + 0.3) + ((((B7 / 1000) / 2) * math.pi) * 0.06)]
        # Если нерж или ХМ коэф = 1.2
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[28][1] *= 1.2
            
        # 29. Роспуск отходов
        self.hours[29] = ['zagotovka_waste_disposal', (C7 * B6 + ((((B7 / 1000) / 2) * math.pi))) * 0.012]
        # 30. Разборка деталей 
        self.hours[30] = ['zagotovka_disassembly_parts', (C7 * B6 + ((((B7 / 1000) / 2) * math.pi))) * ((B5 / 1000) * 7850) * 0.004 * 0.01]
        # 31. Комплектация
        self.hours[31] = ['zagotovka_equipment', (C7 * B6 + ((((B7 / 1000) / 2) * math.pi))) * ((B5 / 1000) * 7850) * 0.006 * 0.01]
        # 32. Маркировка
        self.hours[32] = ['zagotovka_marking', 0.05 * (B6 + 1)]
        # 33. Правка на прессе 
        self.hours[33] = ['zagotovka_press_correction', self.hours[25][1] * 4]
        
        
        # Механическая обработка 
        # 34. Обработка кольцевых стыков
        self.hours[34] = ['mechanical_ring_joint_processing', ((((B7 / 1000) / 2) * math.pi) * 0.7) + ((((B7 / 1000) / 2) * math.pi) * 1.2) + ((((B7 / 1000)) * math.pi) * 0.85) * 1.2]
            
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