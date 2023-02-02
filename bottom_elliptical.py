import math

from . import DB_production as DB
from . import production
    
class BottomEllipticalProduction(production.Production):
    
    def __init__(self, D, Th, steel, parts, lotus=0):
        self.name = 'Днище (элиптическое)'
        self.D = D
        self.Th = Th
        self.parts = parts
        self.noise_koef = 1
        
        self.DB = DB
        
        self.elements = []
        self.elements_hours = []
        
        # Считаем площадь
        #self.S = ((self.D / 1000) * math.pi * (self.Th / 1000))
        self.Dzag = math.sqrt((self.D + self.Th) * (100 + 0.345 * 1.035 * (self.D + self.Th))) * 2
        self.S = (self.Dzag / 1000) * math.pi / 4
        
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
        self.hours[3] = ['cleaning_surface', ((((self.Dzag ** 2) * math.pi) * 2) / 1000000) * 0.036 / 4]
        
        # 4. Зачистка под контроль кромок 
        self.hours[4] = ['edge_control_cleaning', (((self.Dzag * 50 * 4) + (self.D * self.Th * 2)) / 1000000) * 4]
        
        # 5. Обезжиривание 
        self.hours[5] = ['degreasing', (((self.Dzag * 20 * 4) + (self.D * self.Th * 2)) / 1000000) * 2.4]
        
        # 6. Сборка стыка+скобы, клинья (сборка, приварка, срезка) 
        current_assembly_thickness_factor = self.get_coef(self.DB.assembly_thickness_factor, self.Th)
        current_assembly_diametr_factor = self.get_coef(self.DB.assembly_altitude_factor, self.D)
        self.hours[6] = ['assembly', 2 * self.DB.assembly_base_rate * current_assembly_thickness_factor * current_assembly_diametr_factor]
        
        # 7. Подогрев (для обечаек ХМ)
        self.hours[7] = ['heat', 0]
        if self.steel_idx == 3:
            self.hours[7][1] = 0.6
        
        # 8. Прихватка стыка+зачистка
        self.hours[8] = ['seam_tack_cleaning', self.hours[6][1] / 2]
        
        # 9. Сварка стыка 
        self.hours[9] = ['welding', (self.D / 1000) * self.DB.welding_af[self.Th] * 0.175 * 1 * 1.1 * 2]
        
        # 10. Укрытие материалом ( для обечаек ХМ и нерж)
        self.hours[10] = ['cover_meterial', 0]
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[10][1] = 1
        
        # 11. Зачистка (Корень, после каждого прохода, снятие усиления)
        self.hours[11] = ['clearing', 1.62 * (self.Dzag / 1000)]
        
        # 12. Зачистка под контроли 
        self.hours[12] = ['cleanup_under_control', 0.4 * (self.Dzag / 1000) * 2]
        
        # 13. Обрезка борта
        self.hours[13] = ['cut_border', (0.085 * (self.Dzag / 1000) * math.pi) + 0.39]
        
        # 14. Правка (для 2 частей)
        self.hours[14] = ['pravka_many_parts', 0]
        if self.parts > 1:
            self.hours[14][1] = 3.4
            
        # 15. Сборка, сварка и срезка тех. деталей для штамповки (КЗ)
        self.hours[15] = ['assembly_for_stamping', 12.45]
        
        # 16. Штамповка (ШТ)
        self.hours[16] = ['stamping', (((self.Th * 1.5) / 60) + 2 + 0.5) * 3 + 1.6 * 3]
        # Для нержавейки
        if self.steel_idx == 2:
            self.hours[16][1] = (((self.Th * 1) / 60) + 2 + 0.5) * 3
        
        #17. Отжиг и удаление окалины (КЗ)
        self.hours[17] = ['burning_and_burring', (self.Dzag / 1000)**2 * math.pi * 2 * 0.35 * 1.5 / 4]
        
        #18. Зачистка поверхности днища (КЗ) 
        self.hours[18] = ['cleaning_the_hull_surface', 3.45 * ((self.Dzag / 1000) ** 2) * math.pi / 4]
        
        # 1 часть, все материалы
        if self.parts == 1:
            hours = {}
            hours[1] = ['preparation', self.get_hours('preparation')]
            hours[2] = ['check_geometry', self.get_hours('check_geometry')]
            hours[3] = ['cleaning_surface', self.get_hours('cleaning_surface')]
            hours[4] = ['assembly_for_stamping', self.get_hours('assembly_for_stamping')]
            hours[5] = ['stamping', self.get_hours('stamping')]
            hours[6] = ['burning_and_burring', self.get_hours('burning_and_burring')]
            hours[7] = ['cleaning_the_hull_surface', self.get_hours('cleaning_the_hull_surface')]
            self.hours = hours
        
        # 2 части, ХМ
        if self.parts == 2 and self.steel_idx == 3:
            self.set_hours('seam_tack_cleaning', self.get_hours('seam_tack_cleaning') * 1.3)
            self.set_hours('welding', self.get_hours('welding') * 1.3)
            self.set_hours('clearing', self.get_hours('clearing') * 1.3)

        # 2 части, Нерж.
        if self.parts == 2 and self.steel_idx == 2:
            self.set_hours('stamping', self.get_hours('stamping') * 1.2)
            self.set_hours('edge_control_cleaning', self.get_hours('edge_control_cleaning') * 1.2)
            self.set_hours('seam_tack_cleaning', self.get_hours('seam_tack_cleaning') * 1.2)
            self.set_hours('welding', self.get_hours('welding') * 1.2)
            self.set_hours('clearing', self.get_hours('clearing') * 1.2)
            self.set_hours('cleanup_under_control', self.get_hours('cleanup_under_control') * 1.2)
            
        # 3 части
        if self.parts == 3:
            self.set_hours('edge_control_cleaning', self.get_hours('edge_control_cleaning') * 2)
            self.set_hours('degreasing', self.get_hours('degreasing') * 2)
            self.set_hours('assembly', self.get_hours('assembly') * 2)
            self.set_hours('seam_tack_cleaning', self.get_hours('seam_tack_cleaning') * 2)
            self.set_hours('welding', self.get_hours('welding') * 2)
            self.set_hours('clearing', self.get_hours('clearing') * 2)
            self.set_hours('cleanup_under_control', self.get_hours('cleanup_under_control') * 2)
            
        # 3 части, ХМ
        if self.parts == 3 and self.steel_idx == 3:
            self.set_hours('seam_tack_cleaning', self.get_hours('seam_tack_cleaning') * 1.3)
            self.set_hours('welding', self.get_hours('welding') * 1.3)
            self.set_hours('clearing', self.get_hours('clearing') * 1.3)
            self.set_hours('cover_meterial', self.get_hours('cover_meterial') * 1.5)
        
        # 3 части, Нерж.
        if self.parts == 3 and self.steel_idx == 2:
            self.set_hours('stamping', self.get_hours('stamping') * 1.2)
            self.set_hours('edge_control_cleaning', self.get_hours('edge_control_cleaning') * 1.2)
            self.set_hours('seam_tack_cleaning', self.get_hours('seam_tack_cleaning') * 1.2)
            self.set_hours('welding', self.get_hours('welding') * 1.2)
            self.set_hours('clearing', self.get_hours('clearing') * 1.2)
            self.set_hours('cleanup_under_control', self.get_hours('cleanup_under_control') * 1.2)
            self.set_hours('cover_meterial', self.get_hours('cover_meterial') * 2)
            
        # Заготовка
        # 19. Правка
        self.hours[19] = ['zagotovka_edit', self.get_pravka_interpolated() * self.parts]
        # 20. Обход листа
        self.hours[20] = ['zagotovka_tеraverse', ((self.D / 1000) * math.pi) * 0.019 * self.parts]
        # 21. Резка на ЧПУ
        self.hours[21] = ['zagotovka_cut', ((self.D / 1000) * math.pi) * 0.09 * self.parts]
        # Если нерж или ХМ коэф = 1.2
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[21][1] *= 1.2
            
        # 22. Роспуск отходов
        self.hours[22] = ['zagotovka_waste_disposal', ((self.D / 1000) * math.pi) * 0.012 * self.parts]
        # 23. Разборка деталей 
        self.hours[23] = ['zagotovka_disassembly_parts', (((self.D / 1000) * math.pi) * (self.Th / 1000) * 7850) * 0.004 * 0.01 * self.parts]
        # 24. Комплектация
        self.hours[24] = ['zagotovka_equipment', ((self.D / 1000) * math.pi * (self.Th / 1000) * 7850) * 0.006 * 0.01 * self.parts]
        # 25. Маркировка
        self.hours[25] = ['zagotovka_marking', 0.05 * self.parts]
        # 26. Правка на прессе 
        self.hours[26] = ['zagotovka_press_correction', self.get_pravka_interpolated() * 4 * self.parts]
        
        
        # Механическая обработка 
        if self.parts > 1:
            # 27 Обработка продольных кромок
            self.hours[27] = ['mechanical_edge_processing', (self.Dzag / 1000) * (self.Th / 1000) * 2 * 10.23]
            if self.parts > 1:
                self.hours[27][1] = (self.D / 1000) * (self.Th / 1000) * 2 * 10.23 * self.parts
        
        # 28. Обработка кольцевых стыков
        self.hours[28] = ['mechanical_ring_joint_processing', (self.D / 1000) * math.pi * (self.Th / 1000) * 15.73]
        # Если черновая = 0.8
        if self.steel_idx == 1:
            self.hours[28][1] *= 0.8
            
        print(self.hours)
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