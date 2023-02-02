import math

from . import DB_production as DB
from . import production

from . import shell_30_mm
    
class FittingMProduction(production.Production):
    
    def __init__(self, shell_Th, shell_D_in, shell_H, ribs, D, D_in, flange_Th, gussets, gussets_Th, steel, lotus=0):
        self.name = 'Штуцер монтажный'
        self.shell_Th = shell_Th
        self.shell_D_in = shell_D_in
        self.shell_H = shell_H
        self.ribs = ribs
        self.D = D
        self.D_in = D_in
        self.flange_Th = flange_Th
        self.gussets = gussets
        self.gussets_Th = gussets_Th
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
        
        B4 = self.shell_Th
        B5 = self.shell_D_in
        B6 = self.shell_H
        B7 = self.ribs
        B8 = self.D
        C8 = self.D_in
        B9 = self.flange_Th
        B10 = self.gussets
        B11 = self.gussets_Th
        
        # Lкромок
        D8 = (B8 / 1000) * math.pi + (C8 / 1000) * math.pi
        #D вн
        F7 = B5 - 3
        #D внутр
        G7 = F7 - ((F7 / 6) * 2)
        # Lкромок
        H7 = (F7 / 1000) * math.pi + (G7 / 1000) * math.pi
        # Площадь
        I7 = (math.pi * (F7 / 1000) ** 2) - (math.pi * (G7 / 1000) ** 2)
        
        # Lкромок
        C11 = (math.sqrt((((F7 -G7) / 2) ** 2) + (((F7 - G7) / 2) ** 2)) + (F7 - G7)) / 1000
        # Площадь
        D11 = (((F7 - G7) / 1000) * ((F7 - G7) / 1000)) / 2
        # Площадь
        E8 = (math.pi * (B8 / 1000) ** 2) - (math.pi * (C8 / 1000) ** 2)
        
        
        
        # 1. Подготовка места 
        self.hours[1] = ['preparation', 1.0]
        
        # 2. Выложить карту, проверить геометрию
        self.hours[2] = ['check_geometry', 1.5]
        
        # 3. Разметка главных осей
        self.hours[3] = ['main_axes_marking', 0.55 * (B7 + 2)]
        
        # 4. Зачистка кромок +Обезжиривание
        self.hours[4] = ['edge_cleaning_degreasing', (((((B5 + B4 * 2) / 1000) * math.pi) * 2) + ((B5 / 1000) * math.pi * 3) + ((F7 - G7) / 1000)) * 0.15]
        
        #5. Сборка и сварка технологических деталей
        self.hours[5] = ['assembly_welding_technological_parts', 2]
        
        #6. Сборка стыка обечайки и ребер
        assembling_joint_shell_ribs = self.get_assembling_joint_shell_ribs()
        self.hours[6] = ['assembling_joint_shell_ribs', assembling_joint_shell_ribs]
        
        #7. Сварка стыка обечайки и ребер
        welding_joint_shell_ribs = self.DB.welding_madp_30_mm[self.shell_Th]
        self.hours[7] = ['welding_joint_shell_ribs', ((B5 / 1000) * math.pi) * welding_joint_shell_ribs * 1.5 * 0.55 * 1.2 * 1.2 * 0.8 * 3]
        
        #8. Зачистка шва
        self.hours[8] = ['cleaning_seam', 0.75 * ((B5 / 1000) * math.pi) * 3]
        
        #9. Зачистка под контроли 
        self.hours[9] = ['cleanup_under_control', 0.4 * ((B5 / 1000) * math.pi) * 3]
        
        #10. Сварка  стыка  обечайки и фланца
        self.hours[10] = ['welding_shell_flange_joint', ((((B5 + 2 * B4) / 1000) * math.pi) * self.DB.welding_madp_30_mm[self.shell_Th] * 1.5 * 0.55 * 1.2 * 1.2 * 0.8)]
        
        #11. Зачистка шва
        self.hours[11] = ['cleaning_seam', 0.75 * ((((B5 + 2 * B4) / 1000) * math.pi))]
        
        #12. Зачистка под контроли 
        self.hours[12] = ['cleanup_under_control', 0.4 * ((((B5 + 2 * B4) / 1000) * math.pi))]
        
        #13. Сборка косынок с обечайкой и фланцем 
        self.hours[13] = ['assembly_gussets_shell_flange', 0.05 * B10]
        
        #14. Сварка  стыка  обечайки и фланца
        self.hours[14] = ['welding_shell_flange_joint', ((F7 - G7) / 1000) * B10 * self.DB.welding_madp_30_mm[self.shell_Th] * 1.5 * 0.55 * 1.2 * 1.2 * 0.8]
        
        #15. Зачистка шва
        self.hours[15] = ['cleaning_seam', 0.75 * ((F7 - G7) / 1000) * B10]
        
        #16. Зачистка под контроли 
        self.hours[16] = ['cleanup_under_control', 0.4 * ((F7 - G7) / 1000) * B10]
        
        ################################## Фланец       
        # 17. Заготовка
        # 17.1 Правка
        self.hours[17] = ['zagotovka_edit', self.get_pravka_interpolated(D8, B9) * self.ribs]
        # 17.2 Обход листа
        self.hours[18] = ['zagotovka_tеraverse', D8 * 0.019 * self.ribs]
        # 17.3 Резка на ЧПУ
        self.hours[19] = ['zagotovka_cut', D8 * 0.09 * self.ribs]
        # Если нерж или ХМ коэф = 1.2
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[19][1] *= 1.2
        # 17.4 Роспуск отходов
        self.hours[20] = ['zagotovka_waste_disposal', D8 * 0.012 * self.ribs]
        # 17.5 Разборка деталей 
        self.hours[21] = ['zagotovka_disassembly_parts', (E8 * (B9 / 1000) * 7850) * 0.004 * 0.01 * self.ribs]
        # 17.6 Комплектация
        self.hours[22] = ['zagotovka_equipment', (E8 * (B9 / 1000) * 7850) * 0.006 * 0.01 * self.ribs]
        # 17.7 Маркировка
        self.hours[23] = ['zagotovka_marking', 0.05 * self.ribs]
        # 17.8 Правка на прессе 
        self.hours[24] = ['zagotovka_press_correction', self.hours[17][1] * 2 * self.ribs]
        # Механическая обработка 
        # 18 Обработка плоскости и диаметров
        self.hours[25] = ['mechanical_surface_diameter', ((B8 / 1000) * math.pi + (C8 / 1000) * math.pi) * B9 * 0.0072 * self.ribs]
        #########################################
        
        ################################## Ребра       
        # 19. Заготовка
        # 19.1 Правка
        self.hours[26] = ['zagotovka_edit', self.get_pravka_interpolated(H7, B4) * self.ribs]
        # 19.2 Обход листа
        self.hours[27] = ['zagotovka_tеraverse', H7 * 0.019 * self.ribs]
        # 19.3 Резка на ЧПУ
        self.hours[28] = ['zagotovka_cut', H7 * 0.09 * self.ribs]
        # Если нерж или ХМ коэф = 1.2
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[28][1] *= 1.2
        # 19.4 Роспуск отходов
        self.hours[29] = ['zagotovka_waste_disposal', D8 * 0.012 * self.ribs]
        # 19.5 Разборка деталей 
        self.hours[30] = ['zagotovka_disassembly_parts', (I7 * (B4 / 1000) * 7850) * 0.004 * 0.01 * self.ribs]
        # 19.6 Комплектация
        self.hours[31] = ['zagotovka_equipment', (I7 * (B4 / 1000) * 7850) * 0.006 * 0.01 * self.ribs]
        # 19.7 Маркировка
        self.hours[32] = ['zagotovka_marking', 0.05 * self.ribs]
        # 19.8 Правка на прессе 
        self.hours[33] = ['zagotovka_press_correction', self.hours[17][1] * 2 * self.ribs]
        # Механическая обработка 
        # 20 Обработка плоскости и диаметров
        self.hours[34] = ['mechanical_surface_diameter', ((F7 / 1000) * math.pi + (G7 / 1000) * math.pi) * B4 * 0.0072 * self.ribs]
        #########################################
        
        ################################## Косынки       
        # 21. Заготовка
        # 21.1 Правка
        self.hours[35] = ['zagotovka_edit', self.get_pravka_interpolated(B11, D11) * self.gussets]
        # 21.2 Обход листа
        self.hours[36] = ['zagotovka_tеraverse', C11 * 0.019 * self.gussets]
        # 21.3 Резка на ЧПУ
        self.hours[37] = ['zagotovka_cut', C11 * 0.09 * self.gussets]
        # Если нерж или ХМ коэф = 1.2
        if self.steel_idx == 2 or self.steel_idx == 3:
            self.hours[37][1] *= 1.2
        # 21.4 Роспуск отходов
        self.hours[38] = ['zagotovka_waste_disposal', D8 * 0.012 * self.gussets]
        # 21.5 Разборка деталей 
        self.hours[39] = ['zagotovka_disassembly_parts', D11 * (B11 / 1000) * 7850 * 0.004 * 0.01 * self.gussets]
        # 21.6 Комплектация
        self.hours[40] = ['zagotovka_equipment', (D11 * (B11 / 1000) * 7850) * 0.006 * 0.01 * self.gussets]
        # 21.7 Маркировка
        self.hours[41] = ['zagotovka_marking', 0.05 * self.gussets]
        # 21.8 Правка на прессе 
        self.hours[42] = ['zagotovka_press_correction', self.hours[17][1] * 2 * self.gussets]
        #########################################
        
        # ИТОГ
        self.total_hours = sum([i[1] for i in self.hours.values()])
        
        # Расчет обечаек
        shells_hours = 0
        shell_parts = 1
        if self.shell_D_in > 2000:
            shell_parts = 2
        shell1 = shell_30_mm.ShellProduction_30_mm(D=self.shell_D_in, H=self.shell_H, Th=self.shell_Th, steel=self.steel, parts=shell_parts, lotus=0)
        shell1.calc_hours()
        shells_hours += shell1.total_hours
        self.elements.append(shell1)
        print('Н.Ч. на обечайки: ', shell1.total_hours)
        self.total_hours += shells_hours
        
        # Формируем массив расчетов для всех элементов
        for i in self.elements:
            self.elements_hours.append([i.name, i.hours, i.total_hours])
        
        
    def get_assembling_joint_shell_ribs(self):
        try:
            i_prev = 0
            for i in sorted(self.DB.assembling_joint_shell_ribs.keys()):
                if i > self.shell_Th:
                    k_prev = 0
                    for k in sorted(self.DB.assembling_joint_shell_ribs[i_prev].keys()):
                        if k > self.shell_D_in:
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

        
    def get_pravka_interpolated(self, S, Th):
        try:
            i_prev = 0
            for i in sorted(self.DB.pravka.keys()):
                if i > S:
                    k_prev = 0
                    for k in sorted(self.DB.pravka[i_prev].keys()):
                        if k > Th:
                            break
                        k_prev = k
                    break
                i_prev = i
            k_prev_v = self.DB.pravka[i_prev][k_prev]
            k_v = DB.pravka[i][k]
            return (k_prev_v + k_v) / 2
        except:
            return 0.8