"""Библиотека Genetic Algorithm представляет из себя ядро генетического алгоритма.

Основные функции обекта GA не определны и определяются из вне:
    generation_person(GA) -> void # Генерация особои
    selection(GA) -> void # Формирование отбора из популяции
    crossing(GA) -> void # Скрещивание отобранных особей
    mutation(GA) -> void # Мутация потомка, скрещиваемых особей
    def_quality(GA), Person[]) -> Void #Определение качества текущей популяции
    is_end(GA) -> bool # Условие завершения поиска

"""

from param import *
import random
import threading

random.seed()

class GA(object):
    """Класс генетического алгоритма.
    атрибуты:
        last_population #последняя популяция.
        last_selected #последний отбор.
        last_crossed #последний потомок.
        the_best_person_of_population #лучшая особь в текущем поколоении.
        the_best_person #лучшая особь.
    """

    def __init__(self):
        """Конструктор"""

        # Переменные
        self.past_population:'прошлые популяции' = []
        self.last_population:'последняя популяция' = [Person()]
        self.last_selected:'последний отбор' = [Person()]
        self.last_crossed:'последний потомок' = Person()
        self.last_mutated:'последний мутированный' = Person()
        self.the_best_person_of_population:'лучшая особь в текущем поколоении' = Person()
        self.the_best_person:'лучшая особь' = Person()

        self.index_iter:'количество итераций' = 0
        self.last_quality:'последнее качество' = [0,0]
        
        # Внешние функции 
        self.generation_person:'Генерация особои' = lambda self=self: None
        self.selection:'Формирование отбора из популяции' = lambda self=self: None
        self.crossing:'Скрещивание отобранных особей' = lambda self=self: None
        self.mutation:'Мутация потомка, скрещиваемых особей' = lambda self=self: None
        self.def_quality:'Определение качества текущей популяции' = lambda self=self: None
        self.is_end:'Условие завершения поиска' = lambda self=self: None

        pass

    def preparing(self):
        """Генерация нулевой (начальной) популяции.
            Данный метод необходимо выполнять перед началом работы алгоритма
        """
        self.last_population.clear()

        for i in range(param_size_of_population.value):    # Генерация нулевой популяции
            self.generation_person(self)

        self.def_quality(self)    # Определения качества осбей популяции

        self.last_population.sort()    # Сортировка популяции  по качеству в порядке уменьшения

        # self.show_last_population()

        if self.the_best_person < self.last_population[0]:    # Обновление глобальной лучшей особи 
            self.the_best_person = Person(self.last_population[0])

        self.the_best_person_of_population = Person(self.last_population[0])    # Обновление локальной лучшей особи
        
        self.past_population.append(list([Person(i) for i in self.last_population]))

        pass

    def start(self):
        """Цикличное выполнения алгоритма"""

        while True:    # Выполнения в цикле итераций алгоритма
            if self.iteration(): break

        pass

    def iteration(self):
        """Поитерационное выполнение алгоритма"""
        
        if self.is_end(self):    # Проверка выполнения условий завершения работы алгоритма 
            return True

        self.definition_new_population()    # Формирование новой популяции

        # self.show_last_population()
        # self.show_last_the_best_person()
        # self.show_the_best_person()

        if self.the_best_person < self.last_population[0]:    # Обновление глобальной лучшей особи 
            self.the_best_person = Person(self.last_population[0])

        self.the_best_person_of_population = Person(self.last_population[0])    # Обновление локальной лучшей особи
        
        self.past_population.append(list([Person(i) for i in self.last_population]))

        return False

    def definition_new_population(self):
        """Формирование нового поколения"""

        population = []    # локальное хранилище новой популяции

        # self.show_last_population(show=True)

        for i in range(len(self.last_population)):    # Определение потомка (одна итерация)
            self.selection(self)    # Отбор особей для скрещивания
            self.crossing(self)    # Скрещивание, отобранных особей - получение потомка
            self.mutation(self)    # Мутация потомка
            population.append(self.last_mutated)    # Добавление мутированной особи в локальное хранилище новой популяции 

        self.last_population = list(population)    # Загрузка особей из локального хранилища популяции в глобальное
        
        # self.show_last_population(show=True)

        self.def_quality(self)    # Определения качества осбей популяции

        self.last_population.sort(reverse=True)    # Сортировка популяции  по качеству в порядке уменьшения
        pass

    def show_last_population(self, show=False):
        print('Текущая популяция')
        for person in self.last_population:
            person.show(is_chromo_showed = show)

    def show_last_the_best_person(self, show=False):
        print ('Лучшая текущего поколения')
        self.the_best_person_of_population.show(is_chromo_showed = show)

    def show_the_best_person(self, show=False):
        print ('Лучшая за все время')
        self.the_best_person.show(is_chromo_showed = show)

    pass

class Person(object):
    """Класс особи
    атрибуты:
        - хромосомы.
        - качество.
    """

    def __init__(self, person=None):
        """Конструктор"""

        self.__chromosomes = []
        self.quality = 0
        if person != None:
            for cromo in person.chromos: 
                self.add_chromo(list(cromo))
            self.quality = person.quality  

        pass 

    @property
    def chromos(self):
        """Набор хромосом особи (не копия)"""
        return self.__chromosomes
    @chromos.setter
    def chromos(self, chromos): self.__chromosomes = list(chromos)

    def add_chromo(self, crhomo=[]):
        """Добавление хромосомы  в  конец списка"""
        self.__chromosomes.append(list(crhomo))

    def del_chromo(self,index=0):
        """Удалние хромосомы по номеру."""
        self.__chromosomes.pop(index)

    def set_chromo(self,index=0, chromo=[]):
        """Изменение хромосомы с номером 'index' на копию объекта 'chromo'."""
        self.__chromosomes[index] = list(chromo)

    def get_chromo(self,index=0):
        """Получение исходной хромосомы (не копии) с номером 'index'."""
        return self.__chromosomes[index]

    def clear_chromos(self):
        """Очистка хромосом особи"""
        self.__chromosomes.clear()

    def show(self, text='', is_chromo_showed=False):
        str_ = text
        if is_chromo_showed: str_ += str(self.__chromosomes) + ' '
        str_ += 'q:' + str(round(self.quality, 4))
        print(str_)

    def __lt__(self, other): return self.quality < other.quality
    def __le__(self, other): return self.quality <= other.quality
    def __gt__(self, other): return self.quality > other.quality
    def __ge__(self, other): return self.quality >= other.quality
    def __eq__(self, other): 
        if other == None: return type(self) == None
        return self.__chromosomes == other.__chromosomes

    pass


"""Примеры подгружаемых методов:
    - test_generation_person(self = GA());
    - test_definition_quality(self = GA());
    - test_selection(self = GA());
    - test_crossing(self = GA());
    - test_mutation(self = GA());
    - test_end(self = GA());
"""

def test_generation_person(self=GA()):
    """Тестовый метод генерации особи.
    
    Метод предполагает генерацию особи с одной хромосомой.
    
    """

    size = param_size_of_chromosom.value    # Размер хромосомы генерируемой особи

    person = Person()

    person.add_chromo([random.randint(0,1) for i in range(size)])

    self.last_population.append(Person(person))

    pass

def test_definition_quality(self=GA()):
    """ """

    for person in self.last_population:
        quality = 0
        
        for chromo in person.chromos:
            for gene in chromo:
                quality += gene

        person.quality = quality/len(person.chromos[0])

    pass

def test_selection(self=GA()):
    """ """

    size = param_size_of_selection.value

    selected = [] 

    for i in range(size):
        selected.append(
                    Person(self.last_population[random_(len(self.last_population))])
                    )

    self.last_selected = list(selected)

    pass

def test_crossing(self=GA()):
    """ """

    crossed = Person()

    chromo = self.last_selected[0].chromos[0]

    for i in range(0,len(chromo), 2):
        chromo[i] = self.last_selected[1].chromos[0][i]

    crossed.add_chromo(chromo)

    self.last_crossed = Person(crossed)

    pass

def test_mutation(self=GA()):
    """ """

    chance = param_chance_of_mutation.value

    mutated = Person()

    for chromo in self.last_crossed.chromos:
        chr = []

        for gene in chromo:
            if chance > random.random():
                chr.append((gene - 1) * (gene - 1))
            else: 
                chr.append(gene)

        mutated.add_chromo(list(chr))

    self.last_mutated = Person(mutated)
    
    pass

index_iter = [0]
last_quality = [0,0]
def test_end(self = GA()):
    index_iter[0] += 1
    
    if param_count_of_iters.value != 0 and index_iter[0] >= param_count_of_iters.value: 
        return True

    if param_min_of_quality.value != 0 and self.the_best_person_of_population.quality >= param_min_of_quality.value: 
        return True

    if param_iter_without_up.value != 0 and last_quality[1] >= param_iter_without_up.value: 
        return True
    elif param_iter_without_up.value != 0:
        if last_quality[0] < self.the_best_person_of_population.quality:
            last_quality[1] = 0
            last_quality[0] = self.the_best_person_of_population.quality
        else:
            last_quality[1] += 1
    return False


def random_(size):
    x = random.random()
    return int((x**2 + 2*x*(1-param_probab_distr.value)*(1-x))*(size-1))

def test_():
    index_iter[0] = 0
    last_quality[0] = 0
    last_quality[1] = 0

    ga = GA()

    ga.generation_person = test_generation_person
    ga.selection = test_selection
    ga.crossing = test_crossing
    ga.mutation = test_mutation
    ga.def_quality = test_definition_quality
    ga.is_end = test_end

    return ga

def main():

    ga = GA()

    ga.generation_person = test_generation_person
    ga.selection = test_selection
    ga.crossing = test_crossing
    ga.mutation = test_mutation
    ga.def_quality = test_definition_quality
    ga.is_end = test_end
    
    ga.preparing()
    
    for i in range(100):
        

        ga.iteration()

        print('')

        ga.show_last_the_best_person(show=True)
        
        ga.show_the_best_person(show=True)
        

    pass

if __name__ == '__main__': main()