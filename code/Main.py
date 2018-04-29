from genetic_algorithm import *
from param import *
from system import *
import random
import GUI
import datetime
# import openpyxl
# import shutil
import sys

random.seed()


#################| Функции для ГА
def generation_person(self):
    """Добавление новой особи в популяции"""

    size = param_size_of_chromosom.value    # Размер хромосомы генерируемой особи

    person = Person()

    person.add_chromo([random.randint(0,1) for i in range(size)])

    self.last_population.append(Person(person))

    pass
def definition_quality(self):
    """Определение качества для последней популяции"""

    for person in self.last_population:
        chromo = person.chromos[0]
        quality = chromo[0]

        for index in range(len(chromo)-1):
            if chromo[index] == chromo[index+1] and chromo[index+1] == 1:
                quality += 1

        person.quality = quality/len(chromo)

    pass
def selection(self):
    """Отбор из последней популяции"""
    
    
    size = param_size_of_selection.value  # Количество отбираемых особей

    selected = []  # Отобранные особи

    persons_for_selection = []  # Отбираемые особи
    
    # print(self.past_population[-(param_generation_in_selection.value):])

    for popul in self.past_population[-(param_generation_in_selection.value):]:    
        # добавление на отбор особей последних поколений
        for person in popul:
            persons_for_selection.append(Person(person))
            # print(persons_for_selection)

    persons_for_selection.sort(reverse=True)    # сортировка особей
    

    if param_add_best:    # Проверка необходимости добавлять лучшую особь в отбор
        self.last_selected.append(Person(self.the_best_person))

    if param_add_repeat:  # Добавление с повторными
        while len(selected) < size: 
            selected.append(
                    Person(
                        persons_for_selection[random_(len(persons_for_selection))]
                    )
            )
    else:  # Добавление без повторных
        while len(selected) < size:
            l_person_for_selection = []
            for pers in persons_for_selection:
                if selected.count(pers) == 0:
                    l_person_for_selection.append(pers)
            if len(l_person_for_selection) < 1: break
            p = Person(l_person_for_selection[random_(len(l_person_for_selection))])
            selected.append(p)

    self.last_selected = []   # Отчистка прошлого отбора для формирования нового
    self.last_selected = list(selected)
    pass
def crossing(self=GA()):
    """Скрещивание"""

    if param_type_of_crossing.value == 1:    # Блок обработки первого типа скрещивания
        """
            Точечное скрещивание с фиксированным разрывом. 

            Данный тип предполагает разрыв хромосомных пар сращиваемых особей в 
            точке разрыва и соединение их разных частей в общую хромосому. 
            Позиция и количество разрывов остается неизменным на протяжении всей операции скрещивания

        """

        # Минимальное кол-ао точек разрыва равно: (размер отбора) - 1
        # Максимальное кол-ао точек разрыва равно: (размер хромосомы) - 1
        # self.last_selected.sort(reverse=False)

        validBPPos = [i for i in  range(param_size_of_chromosom.value-1)]
        breakpoints = []
        for i in range(param_count_of_breakpoints.value):  # Генерация точек разрыва
            randIndex = random.randint(0,len(validBPPos)-1)
            breakpoints.append(validBPPos[randIndex])
            validBPPos.pop(randIndex)
        breakpoints.sort()
        index_gene = 0  # Индекс гена
        index_pers = 0  # Индекс особи
        index_bp = 0  # Индекс точки разрыва
        chromo = []
        while index_gene < param_size_of_chromosom.value:
            if breakpoints[index_bp] < index_gene:  # Проверка достижения точки разрыва
                index_bp += 1
                index_pers += 1
            if index_pers >= len(self.last_selected):  # Сброс индекса особи
                index_pers = 0
            if index_bp >= param_count_of_breakpoints.value:  # Проверка исчерпания списка точек селекции
                pers = Person(self.last_selected[index_pers])
                chromo.extend(pers.get_chromo(0)[breakpoints[index_bp-1]+1:])
                break
            pers = Person(self.last_selected[index_pers])
            chromo.append(pers.get_chromo(0)[index_gene])
            index_gene += 1
        self.last_crossed = Person()
        self.last_crossed.add_chromo(chromo)
        pass

    if param_type_of_crossing.value == 2:    # Блок обработки второго типа скрещивания

        """

            Точечное попарное скрещивание с динамическим разрывом. 

            Данный тип скрещивания предполагает попарное скрещивание особей с изменением 
            позиций точек разрыва для каждой пары. Количество разрывов 
            остается не именным на протяжении всей операции скрещивания.

        """

        self.last_selected.sort(reverse=True)
        l_selected = [0, 0]
        l_selected[1] = list(self.last_selected[len(self.last_selected)-1].get_chromo(0))
        for index in range(len(self.last_selected)-1):
            l_selected[0] = list(self.last_selected[index+1].get_chromo(0))
            validBPPos = [i for i in  range(param_size_of_chromosom.value-1)]
            breakpoints = []
            for i in range(param_count_of_breakpoints.value):  # Генерация точек разрыва
                randIndex = random.randint(0,len(validBPPos)-1)
                breakpoints.append(validBPPos[randIndex])
                validBPPos.pop(randIndex)
            breakpoints.sort() 
            index_gene = 0  # Индекс гена
            index_pers = 0  # Индекс особи
            index_bp = 0  # Индекс точки разрыва
            while index_gene < param_size_of_chromosom.value:
                if breakpoints[index_bp] <= index_gene:  # Проверка достижения точки разрыва
                    index_bp += 1
                    index_pers += 1
                if index_pers >= 2:  # Сброс индекса особи
                    index_pers = 0
                if index_bp >= param_count_of_breakpoints.value:  # Сброс индекса точки разрыва
                    index_bp = 0
                l_selected[1][index_gene] = l_selected[index_pers][index_gene]
                index_gene += 1
        self.last_crossed = Person()
        self.last_crossed.add_chromo(l_selected[1])

        pass
    
    pass
def mutation(self):

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
    pass
def end(self):
    self.index_iter += 1
    
    INFO('index of iter %s' % str(self.index_iter))
    INFO('last quality %s' % str(self.last_quality))
    INFO('count past population %s' % str(len(self.past_population)))
    
    if param_count_of_iters.value != 0 and self.index_iter >= param_count_of_iters.value: 
        INFO('end for count iters %s/%s is %s' % (
                    str(self.index_iter),
                    str(param_count_of_iters.value),
                    str(param_count_of_iters.value != 0 and self.index_iter >= param_count_of_iters.value)
            )
        )
        return True

    if param_min_of_quality.value != 0 and self.the_best_person_of_population.quality >= param_min_of_quality.value: 
        INFO('end for min quality %s/%s is %s' % (
                    str(self.the_best_person_of_population.quality),
                    str(param_min_of_quality.value),
                    str(param_min_of_quality.value != 0 and self.the_best_person_of_population.quality >= param_min_of_quality.value)
            )
        )
        return True

    if param_iter_without_up.value != 0 and self.last_quality[1] >= param_iter_without_up.value: 
        return True
    elif param_iter_without_up.value != 0:
        if self.last_quality[0] < self.the_best_person_of_population.quality:
            self.last_quality[1] = 0
            self.last_quality[0] = self.the_best_person_of_population.quality
        else:
            self.last_quality[1] += 1
    return False


def random_(size, shift=param_probab_distr.value):
    """Генерация случайного числа с неровномерным распределением вероятности"""
    x = random.random()
    shift = param_probab_distr.value
    return int((x**2 + 2*x*(1-shift)*(1-x))*(size-1))


def SaveResult(qualities=[1,2,3,4], persons=[[]]):
    """Сохранение результатов"""

    dt = str(datetime.datetime.now()).replace(':','_')

    file = open('results\%s_qualities.txt' % dt, 'w')
    file_1 = open('results\%s_persons.txt' % dt, 'w')
    
    text = ''
    text += '\n ========================|PARAMS|========================'
    text += '\n s_cromosom: %s      // Размер хромосомы' %                          param_size_of_chromosom.value
    text += '\n s_population: %s    // Размер популяции' %                          param_size_of_population.value
    text += '\n s_selection: %s     // Размер отбора' %                             param_size_of_selection.value
    text += '\n g_selection: %s     // Поколений в отборе' %                        param_generation_in_selection.value
    text += '\n ch_mutation: %s     // Шанс мутации' %                              param_chance_of_mutation.value
    text += '\n ch_distribution: %s // Распределение вероятности' %                 param_probab_distr.value
    text += '\n select_repeat: %s   // Участие повторяющихся особей в отборе' %     param_add_repeat.value
    text += '\n select_best: %s     // Участие лучшей особи в отборе' %             param_add_best.value
    text += '\n c_breakpoints: %s   // Количество точек разрыва' %                  param_count_of_breakpoints.value
    text += '\n t_crossing: %s      // Тип скрещивания' %                           param_type_of_crossing.value
    text += '\n c_iteration: %s     // Количество итераций для остоновки' %         param_count_of_iters.value
    text += '\n search_quality: %s  // Искомое качество' %                          param_min_of_quality.value
    text += '\n w_up: %s            // Количество итераций без роста' %             param_iter_without_up.value
    text += '\n ======================|QUALITIES|======================='
    
    
    for index in range(len(qualities)):
        text += '\n' + str(qualities[index])
    file.write(text.replace('.',','))
    file.close()

    text_1 = ''
    for index in range(len(persons)):
        text_1 += '%i\t%s\n' % (index,str(persons[index]))
    file_1.write(text_1.replace('\'','').replace(' ','').replace(',','').replace('.',''))
    file_1.close()

    pass
def SaveExcelResultReport(qualities=[[]]):

    wb = openpyxl.load_workbook('reportex.xlsx')
    sheet = wb['list']

    sheet.cell(row=5, column=13).value = 's_cromosom: %s      ' % param_size_of_chromosom.value
    sheet.cell(row=6, column=13).value = 's_population: %s    ' % param_size_of_population.value
    sheet.cell(row=7, column=13).value = 's_selection: %s     ' % param_size_of_selection.value
    sheet.cell(row=8, column=13).value = 'g_selection: %s     ' % param_generation_in_selection.value
    sheet.cell(row=9, column=13).value = 'ch_mutation: %s     ' % param_chance_of_mutation.value
    sheet.cell(row=10, column=13).value = 'ch_distribution: %s ' % param_probab_distr.value
    sheet.cell(row=11, column=13).value = 'select_repeat: %s   ' % param_add_repeat.value
    sheet.cell(row=12, column=13).value = 'select_best: %s     ' % param_add_best.value
    sheet.cell(row=13, column=13).value = 'c_breakpoints: %s   ' % param_count_of_breakpoints.value
    sheet.cell(row=14, column=13).value = 't_crossing: %s      ' % param_type_of_crossing.value
    sheet.cell(row=15, column=13).value = 'c_iteration: %s     ' % param_count_of_iters.value
    sheet.cell(row=16, column=13).value = 'search_quality: %s  ' % param_min_of_quality.value
    sheet.cell(row=17, column=13).value = 'w_up: %s            ' % param_iter_without_up.value

    for i in range(len(qualities)):
        for j in range(len(qualities[i])):
            sheet.cell(row=2+j, column=15+i).value = qualities[i][j]

    wb.save('results\%s.xlsx' % str(datetime.datetime.now()).replace(':','_'))    
    pass
def SaveExcelResultReportOne(qualities=[]):

    wb = openpyxl.load_workbook('reportexone.xlsx')
    sheet = wb['list']

    sheet.cell(row=5, column=13).value = 's_cromosom: %s      ' % param_size_of_chromosom.value
    sheet.cell(row=6, column=13).value = 's_population: %s    ' % param_size_of_population.value
    sheet.cell(row=7, column=13).value = 's_selection: %s     ' % param_size_of_selection.value
    sheet.cell(row=8, column=13).value = 'g_selection: %s     ' % param_generation_in_selection.value
    sheet.cell(row=9, column=13).value = 'ch_mutation: %s     ' % param_chance_of_mutation.value
    sheet.cell(row=10, column=13).value = 'ch_distribution: %s ' % param_probab_distr.value
    sheet.cell(row=11, column=13).value = 'select_repeat: %s   ' % param_add_repeat.value
    sheet.cell(row=12, column=13).value = 'select_best: %s     ' % param_add_best.value
    sheet.cell(row=13, column=13).value = 'c_breakpoints: %s   ' % param_count_of_breakpoints.value
    sheet.cell(row=14, column=13).value = 't_crossing: %s      ' % param_type_of_crossing.value
    sheet.cell(row=15, column=13).value = 'c_iteration: %s     ' % param_count_of_iters.value
    sheet.cell(row=16, column=13).value = 'search_quality: %s  ' % param_min_of_quality.value
    sheet.cell(row=17, column=13).value = 'w_up: %s            ' % param_iter_without_up.value

    for i in range(len(qualities)):
        sheet.cell(row=2+i, column=14).value = qualities[i]

    wb.save('results\ONE_%s.xlsx' % str(datetime.datetime.now()).replace(':','_'))    
    pass


def main():
    """Первоисполняемый метод"""

    if len(sys.argv) == 1 or sys.argv[1] == 'GUI':
        GUI.ManagerOfScreens.start()
    elif sys.argv[1] == 'WGUI':
        GUI.WithOutGUI()

    pass

if __name__ == '__main__': main()




