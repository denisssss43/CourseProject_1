"""Параметры.

Глобальные параметры системы.

Параметры системы:
    - Размер хромосомы 
    - Размер популяции 
    - Вероятность мутации
    Селекция:
      - Распределение вероятности
      - Повторения в отборе
      - Учет лучшего
      - Размер отбора
      - Поколений в отборе
    Условия остановки:
      - Количество итераций
      - Порог качества
      - Итерация без роста 
    Скрещивание:
      - Тип скрещивания 
      - Количество точек разрыва
"""

class Param(object):
    """Параметр системы"""

    params = []    # Глобальное хранилище параметров

    def __init__(self, value): 
        """Конструктор особи"""

        self.param = {'id':len(Param.params),'value':value}    # Загрузка атрибутов конструктора в параметры объекта

        Param.params.append(self.param)    # Добавление параметров объекта вглобальный список параметров
        
        pass
        
    @property
    def value(self): 
        return self.param['value']    # Возврат значения парамтра
    @value.setter
    def value(self, v): 
        ## print(
        ##     'LOG INFO: param id %s changed value %s to %s' % (
        ##       str(self.param['id']), 
        ##       str(self.param['value']), 
        ##       str(v)
        ##   )
        ## )
        self.param['value'] = v    # Прием значения параметра

    pass

# блок общих параметров ГА
param_size_of_chromosom:'Размер хромосомы' = Param(75)
param_size_of_population:'Размер популяции' = Param(20)
param_chance_of_mutation:'Вероятность мутации' = Param(.01)

# блок общих параметров ГА-селекции
param_probab_distr:'Распределение вероятности' = Param(1.0)
param_add_repeat:'Повторения в отборе' = Param(False)
param_add_best:'Учет лучшего' = Param(False)
param_size_of_selection:'Размер отбора' = Param(10)
param_generation_in_selection:'Поколений в отборе' = Param(1)

# блок общих параметров ГА-скрещивания
param_type_of_crossing:'Тип скрещивания' = Param(2)
param_count_of_breakpoints:'Количество точек разрыва' = Param(9)

# блок общих параметров ГА-остановки 
param_count_of_iters:'Количество итераций' = Param(200)
param_min_of_quality:'Порог качества' = Param(0)
param_iter_without_up:'Итерация без роста' = Param(0)


# системные параметры
is_end_run_app:'Необходимость завершить выполнения программы' = {'value':False}
