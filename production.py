class Production():
    
    OPERATIONS = {
        'preparation' : ['Подготовка места', ''], #1
        'check_geometry' : ['Выложить, проверить геометрию', ''], #2
        'cleaning_surface' : ['Очистка поверхности развертки', ''], #3
        'rolling' : ['Вальцовка (подготовка и вальцовка)', ''], #4
        
        'assembly_and_welding_of_rigging_elements' : ['Сборка, сварка строповочных элементов', ''],
        'cutting_allowances' : ['Разметка, срезка припуска, доводка фасок', ''],
        'welding_lid_and_petals' : ['Сварка стыка крышки и лепестков', ''],
        'welding_petals' : ['Сварка стыков лепестков', ''],
        'assembly_of_petal_joints' : ['Сборка стыков лепестков (скобы, клинья, сборка, приварка, срезка)', ''],
        'assembly_of_the_lid_and_petals' : ['Сборка стыка крышки и лепестков (скобы, клинья, сборка, приварка, срезка)', ''],
        'technological_components' : ['Технологичческие детали', ''],
        
        'markup' : ['Разметка', ''], #5
        'edge_control_cleaning' : ['Зачистка под контроль кромок', ''], #5
        'cut_border' : ['Обрезка борта', ''], #6
        'degreasing' : ['Обезжиривание', ''], #7
        'assembly' : ['Сборка стыка + скобы, клинья (сборка, приварка, срезка)', ''], #8
        'seam_tack_cleaning' : ['Прихватка стыка + зачистка', ''], #9
        'welding' : ['Сварка стыка', ''], #10
        'clearing' : ['Зачистка (Корень, после каждого прохода, снятие усиления)', ''], #11
        'calibration' : ['Калибровка', ''], #12
        'cleanup_under_control' : ['Зачистка под контроли', ''], #13
        'ovality' : ['Выведение овальности', ''], #14
        'heat' : ['Подогрев (для обечаек ХМ)', ''], #15
        'cover_meterial' : ['Укрытие материалом (для обечаек ХМ и нерж.)', ''], #16
        'pravka_many_parts' : ['Правка', ''], #17
        
        'assembly_for_stamping' : ['Сборка, сварка и срезка тех. деталей для штамповки (КЗ)', ''], #18
        'stamping' : ['Штамповка (ШТ)', ''], #19
        'burning_and_burring' : ['Отжиг и удаление окалины (КЗ)', ''], #20
        'cleaning_the_hull_surface' : ['Зачистка поверхности днища (КЗ)', ''], #21
        
        'zagotovka_edit' : ['Заготовка -> Правка', ''], #22
        'zagotovka_guard' : ['Заготовка -> Зачистка от окалины', ''], #22
        'zagotovka_tеraverse' : ['Заготовка -> Обход листа', ''], #23
        'zagotovka_cut' : ['Заготовка -> Резка на ЧПУ', ''], #24
        'zagotovka_waste_disposal' : ['Заготовка -> Роспуск отходов', ''], #25
        'zagotovka_disassembly_parts' : ['Заготовка -> Разборка деталей', ''], #26
        'zagotovka_equipment' : ['Заготовка -> Комплектация', ''], #27
        'zagotovka_marking' : ['Заготовка -> Маркировка', ''], #28
        'zagotovka_press_correction' : ['Заготовка -> Правка на прессе', ''], #29
        'mechanical_edge_processing' : ['Механическая обработка -> Обработка продольных кромок', ''], #30
        'mechanical_ring_joint_processing' : ['Механическая обработка -> Обработка кольцевых стыков', ''], #31
        'mechanical_height_processing' : ['Механическая обработка -> Обработка по высоте', ''], #31
        
        'mechanical_surface_diameter' : ['Механическая обработка -> Обработка плоскости и диаметров', ''], #31 
        
        'main_axes_marking' : ['Разметка главных осей', ''],
        'edge_cleaning_degreasing' : ['Зачистка кромок +Обезжиривание', ''],
        'assembly_welding_technological_parts' : ['Сборка и сварка технологических деталей', ''],
        
        'assembly_ring_joint' : ['Сборка кольцевого стыка', ''],
        'welding_ring_joint' : ['Сварка кольцевого стыка', ''],
        'clearing_root_seam' : ['Зачистка (Корень, шов)', ''], 
        'marking_rings_ribs' : ['Разметка колец и ребер', ''], 
        'assembly_rings_ribs_shells' : ['Сборка колец и ребер с обечайками', ''],
        'welding_rings_ribs' : ['Сварка колец и ребер', ''],
        'cleaning_seam' : ['Зачистка шва', ''],
        'hole_marking' : ['Разметка отверстий', ''],
        'hole_cutting' : ['Резка отверстий', ''],
        'assembly_welding_windows' : ['Сборка и сварка окон', ''],
        'assembly_welding_covers_staples_bosses' : ['Сборка и сварка накладок, скоб и бобышек', ''],
        'assembly_welding_internal' : ['Сборка и сварка внутренних устройств', ''],
        
        'mechanical_fastener_processing' : ['Механическая обработка крепежа', ''],
        
        'assembling_joint_shell_ribs' : ['Сборка стыка обечайки и ребер', ''],
        'welding_joint_shell_ribs' : ['Сварка стыка обечайки и ребер', ''],
        'welding_shell_flange_joint' : ['Сварка  стыка  обечайки и фланца', ''],
        'assembly_gussets_shell_flange' : ['Сборка косынок с обечайкой и фланцем', ''],
        
        'assembling_joint_flange_nozzle' : ['Сборка стыка фланца и патрубка', ''],


    }
    
    def __init__(self):
        pass
    
    # Функция поиска соседних элементов в массиве вида: [ [20, 1.5], [30, 2.1] ]
    def find_neighbours(self, data, x):
        for i in range(1, len(data)):
            if data[i][0] > x:
                return (data[i-1], data[i])
        return (data[0], data[1])
            
    # Функция интерполяции
    def interpolation(self, m, x):
        res = (x - m[0][0]) * (m[1][1] - m[0][1]) / (m[1][0] - m[0][0]) + m[0][1]
        return res
    
    # Сводная функция извлечения коэфициента с интерполяцией
    def get_coef(self, data, x):
        neighbours = self.find_neighbours(data, x)
        res = self.interpolation(neighbours, x)
        return res
    
    
    def get_hours(self, key):
        for i in self.hours.values():
            if key == i[0]:
                return i[1]
        return False
    
    
    def set_hours(self, key, value):
        for i in self.hours.values():
            if key == i[0]:
                i[1] = value
                return True
        return False