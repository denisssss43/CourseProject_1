"""Пользовательский интерфейс (UI)

Состоит из определний окон ПС и дополнительных виджетов.

Определены следующие окна:
    - Главный экран (SMain)
    - Экран настройки селекции (SSettingsOfSelection)
    - Экран настройки скрещивания (SSettingsOfCrossing)
    - Экран настройки завершения (SSettingsOfEnding)
    - Экран сохранения результата (SSaveResult)
    - Экран опций результатов (SOptionsOfResult)
    - Экран сравнения результатов (SComparisonResults)
    - Экран просмотра результатов (SViewResults)

Определены следующие дополнительные виджеты:
    - Виджет графика (WGraph)
    - Виджет слайдер с подписью (WSliderWithSign)
    - Виджет окно с сопроводительной информацией (WInfBox)

"""


from tkinter import *
from genetic_algorithm import *
from param import *
from random import *
from system import *
import threading
from Main import *


class WGraph(object):
    """График"""

    
    def __init__(self, root, pos=[0,0], size=[0,0], padding=[0,0,0,0]):
        self.__canvas:'Конвас для отображения на нем необходимых значений' = Canvas(root, bg='white')
        self.__size:'Размер графика' = size
        self.__padding:'Отступы' = padding
        self.__ranges:'Области значений для построения графика' = [ ]
        self.add_range()

        # INFO: расположение графика на экране
        self.__canvas.place(x=pos[0], y=pos[1], width=size[0], height=size[1])  
        
        # INFO: обновление выводимой на в график информации
        self.update()
        pass
    
    def convas(self):
        return self.__canvas

    def update(self):
        self.__canvas.delete('all')

        max_value = max([max(i['values']) for i in self.__ranges])    # Максимальное значение из заданных областей
        min_value = min([min(i['values']) for i in self.__ranges])    # Минимальное значение из заданных областей

        size = max([len(i['values']) for i in self.__ranges])    # Макисмальное кол-во значений у заданных облостей

        shift = .9    # Отступ от края конваса

        # INFO: лямбды нормализации значений для осей X,Y
        Y = lambda value: (1-self.__padding[0]) * self.__size[1] * (max_value-value)/max_value + self.__size[1] * self.__padding[2]
        X = lambda index: (1-self.__padding[1]) * self.__size[0] * index/(size-1) + self.__size[0] * self.__padding[3]


        index = 0
        for value in self.__ranges:    # Вывод значений
            name = value['name']
            width = value['width']
            fill = value['color']
            values = value['values']
            show_inf = value['inf']
            
            if show_inf:    # Вывод информации по облостям
                index += 1
                self.__canvas.create_text(
                                2, 15*index - 5, 
                                text='%s max:%f min:%f' % (name, max(values), min(values)), 
                                font="Consolas 10",
                                anchor="w",
                                fill=fill)

        index = 0
        for value in self.__ranges:    # Вывод значений
            name = value['name']
            width = value['width']
            fill = value['color']
            values = value['values']
            show_inf = value['inf']
            
            for i in range(len(values) - 1):
                if i == 0: 
                    self.__canvas.create_line(
                                    X(i) + 5, Y(values[i])+5, 
                                    X(i + 1), Y(values[i + 1])+5, 
                                    width=width, 
                                    fill=fill
                                    )
                elif i == len(values) - 2: 
                    self.__canvas.create_line(
                                    X(i), Y(values[i])+5, 
                                    X(i + 1) - 5, Y(values[i + 1])+5, 
                                    width=width, 
                                    fill=fill
                                    )
                else:                
                    self.__canvas.create_line(
                                    X(i), Y(values[i])+5, 
                                    X(i + 1), Y(values[i + 1])+5, 
                                    width=width, 
                                    fill=fill
                                    )

                
        pass

    def add_range(self, name='range',color='blue', width=1, inf=True, values=[i*i*.3 for i in range(10)]):
        self.__ranges.append({
                    'name':name,
                    'values':values,
                    'color':color,
                    'width':width,
                    'inf':inf
                })
        self.update()
        pass
    def clear_ranges(self):
        self.__ranges.clear()
        pass
    
    def add_values(self, index_range, values=[]):
        self.__ranges[index_range]['values'] = values
        self.update()
        pass
    def add_value(self, index_range, value=0):
        self.__ranges[index_range]['values'].append(value)
        self.update()
        pass

    pass
class WSliderWithSign(object):
    """Слайдер с подписью"""

    def __init__(self, 
                 root, 
                 pos=[0,0], length=100,
                 text='text',
                 event_change_value=lambda:print('Значение изменено'),
                 default_value=0,
                 min_value='',
                 max_value='',
                 min=0, max=1, step=1):

        self.__scale = Scale(
                        root, 
                        orient=HORIZONTAL, 
                        length=length, 
                        from_=min, to=max, resolution=step, 
                        command=self.event_upd)
        self.__scale.place(x=pos[0]-3, y=pos[1]+4)
        self.__scale.set(default_value)
        self.__event_change_value = event_change_value
        
        self.__min_value = min_value
        self.__max_value = max_value

        self.__min = min
        self.__max = max

        Label(root, text='').place(x=pos[0], y=pos[1], width=length)

        self.__label = Label(root, text=str(default_value), anchor='e')
        self.__label.place(x=pos[0], y=pos[1], width=length)

        Label(root, text=text).place(x=pos[0], y=pos[1])
        
        self.event_upd()
        
        pass
    

    def value(self):
        return self.__scale.get()

    def event_upd(self, event=None):

        value = str(self.__scale.get())
        if self.__min_value != '' and self.__scale.get() == self.__min:
            value = self.__min_value
        if self.__max_value != '' and self.__scale.get() == self.__max:
            value = self.__max_value

        self.__label['text'] = value
        self.__event_change_value(self)

        pass

    pass
class WInfoBox(object):

    def __init__(self, root, pos=[0,0], size=[0,0]):

        self.__info = Label(
                root, 
                text='', 
                anchor='nw', 
                bg='white')
        self.__info.place(x=pos[0], y=pos[1], width=size[0], height=size[1])

        self.__lines = []

        self.__size = size

        pass
    
    def add_line(self, string):

        while len(self.__lines) > 0 and len(self.__lines) >= int(self.__size[1]/15):
            self.__lines.pop(0)

        self.__lines.append(string)
        self.update()

        pass
    def clear_line(self):

        self.__lines.clear()
        self.update()

        pass

    def update(self):
        self.__info['text'] = '' 
        for string in self.__lines:
            self.__info['text'] += string + '\n'
    pass

class SMain(object):
    """Главный экран"""

    def __init__(self):

        self.__root = Tk()
        self.__root.title('ПЭМС ГА - Д.Р. Карасев')
        self.__root.geometry('800x600')
        self.__root.resizable(width=False, height=False)
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        CenterOnScreen(self.__root, size=[800,600])
        self.__root.focus_force()
        self.__run_ga = False
        
        self.info = WInfoBox(
                        self.__root,
                        pos=[340,480],
                        size=[440,100])

        WSliderWithSign(
                    self.__root, 
                    pos=[20, 20], 
                    length=300, 
                    text='Размер хромосомы',
                    min=5, max=1000, step=1, default_value=param_size_of_chromosom.value,
                    event_change_value=self.event_sld_1)
        WSliderWithSign(
                    self.__root, 
                    pos=[20, 80], 
                    length=300, 
                    text='Размер популяции',
                    min=5, max=100, step=1, default_value=param_size_of_population.value,
                    event_change_value=self.event_sld_2)
        WSliderWithSign(
                    self.__root, 
                    pos=[20, 145], 
                    length=300, 
                    text='Вуроятность мутации',
                    min=0, max=1, step=.001, default_value=param_chance_of_mutation.value,
                    event_change_value=self.event_sld_3)

        self.__graf = WGraph(self.__root, [340,20], [440,440], padding=[.1,0,.2,0])

        Button(
            self.__root, 
            text='Селекция', 
            command=lambda: self.event_btn_1('')
            ).place(
                x=20, y=230, 
                width=300, height=40
                )

        Button(
            self.__root, 
            text='Скрещивания', 
            command=lambda: self.event_btn_2('')
            ).place(
                x=20, y=280, 
                width=300, height=40
                )

        Button(
            self.__root, 
            text='Условие завершения', 
            command=lambda: self.event_btn_3('')
            ).place(
                x=20, y=330, 
                width=300, height=40
                )

        Button(
            self.__root, 
            text='Начало', 
            command=lambda: self.event_btn_4('')
            ).place(
                x=20, y=400,
                width=300, height=40
                )
                
        pass

    def close(self):
        is_end_run_app['value'] = True
        self.__root.destroy()
        pass

    def event_btn_1(self, event):
        ManagerOfScreens.active_screen = SSettingsOfSelection
        self.__root.destroy()
        pass
    def event_btn_2(self, event):
        ManagerOfScreens.active_screen = SSettingsOfCrossing
        self.__root.destroy()
        pass
    def event_btn_3(self, event):
        ManagerOfScreens.active_screen = SSettingsOfEnding
        self.__root.destroy()
        pass
    def event_btn_4(self, event):
        self.info.add_line('Начало')
        
        if self.__run_ga: 
            self.__run_ga = False
            self.act(isActive=NORMAL)
        else:
            self.__run_ga = True
            threading.Thread(target=self.run_ga, daemon=True).start()

        INFO('runing GA is ' + str(self.__run_ga))



        pass
    def event_btn_5(self, event):
        ManagerOfScreens.active_screen = SSaveResult
        self.__root.destroy()
        pass
    def event_btn_6(self, event):

        print('btn_6')
        ManagerOfScreens.active_screen = SOptionsOfResult
        self.__root.destroy()
        pass
    
    def event_sld_1(self, event):
        param_size_of_chromosom.value = event.value()
        pass
    def event_sld_2(self, event):
        param_size_of_population.value = event.value()
        pass
    def event_sld_3(self, event):
        param_chance_of_mutation.value = event.value()
        pass

    def act(self, isActive=DISABLED):
        for i in range(20): 
            self.__root.winfo_children()[len(self.__root.winfo_children())-(i+1)]['state'] = isActive
        
        self.__root.winfo_children()[len(self.__root.winfo_children())-1]['state'] = NORMAL

        if isActive == DISABLED:
            self.__root.winfo_children()[len(self.__root.winfo_children())-1]['text'] = 'Стоп'
        else:
            self.__root.winfo_children()[len(self.__root.winfo_children())-1]['text'] = 'Начать'
        
        pass

    def run_ga(self):
        
        self.act()

        INFO('start GA')
        INFO('runing GA is ' + str(self.__run_ga))

        ga = GA()

        ga.generation_person = generation_person
        ga.selection = selection
        ga.crossing = crossing
        ga.mutation = mutation
        ga.def_quality = definition_quality
        ga.is_end = end

        ga.preparing()

        qualities = [ga.the_best_person_of_population.quality]
        theBestes = [list(ga.the_best_person_of_population.get_chromo())]

        self.__graf.clear_ranges()
        self.__graf.add_range(
                        name='quality',
                        color='blue', 
                        width=2, 
                        inf=True,
                        values=[qualities[len(qualities)-1]]
                        )

        iter = 1

        while not ga.iteration() and self.__run_ga: 
            qualities.append(ga.the_best_person_of_population.quality)
            theBestes.append(list(ga.the_best_person_of_population.get_chromo()))
            self.__graf.add_value(0, qualities[len(qualities)-1])
            self.info.add_line('Итерация: %s (%s)' % (iter, qualities[len(qualities)-1]))
            iter += 1

        self.__run_ga = False
        self.info.add_line('Работа ГА прекращена')
        INFO('runing GA is ' + str(self.__run_ga))

        SaveResult(qualities, theBestes)

        self.act(NORMAL)
        
        pass

    pass
class SSettingsOfSelection(object):
    """Экран настройки селекции"""

    def __init__(self):
        
        self.__root = Tk()
        self.__root.title('Параметры селекции')
        self.__root.geometry('660x380')
        self.__root.resizable(width=False, height=False)
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        CenterOnScreen(self.__root, size=[660,440])
        self.__root.focus_force()

        self.__graf = WGraph(self.__root, [20,20], [300,285])
        
        WSliderWithSign(
                    self.__root, 
                    pos=[340, 20], 
                    length=300, 
                    text='Повторения в отборе',
                    min=False, max=True, default_value=param_add_repeat.value,
                    min_value=False, max_value=True,
                    event_change_value=self.event_sld_1)
        WSliderWithSign(
                    self.__root, 
                    pos=[340, 80], 
                    length=300, 
                    text='Учет лучшего',
                    min=False, max=True, default_value=param_add_best.value,
                    min_value=False, max_value=True,
                    event_change_value=self.event_sld_2)
        WSliderWithSign(
                    self.__root, 
                    pos=[340, 140], 
                    length=300, 
                    text='Размер отбора',
                    min=2, max=25, default_value=param_size_of_selection.value,
                    event_change_value=self.event_sld_3)
        WSliderWithSign(
                    self.__root, 
                    pos=[340, 200], 
                    length=300, 
                    text='Поколений в отборе',
                    min=1, max=20, default_value=param_generation_in_selection.value,
                    event_change_value=self.event_sld_4)
        WSliderWithSign(
                    self.__root, 
                    pos=[340, 260], 
                    length=300, 
                    text='Распределение вероятности',
                    min=0, max=1, step=.01, default_value=param_probab_distr.value,
                    event_change_value=self.event_sld_5)
        
        self.__param_add_repeat = param_add_repeat.value
        self.__param_add_best = param_add_best.value
        self.__param_size_of_selection = param_size_of_selection.value
        self.__param_generation_in_selection = param_generation_in_selection.value
        self.__param_probab_distr = param_probab_distr.value

        btm = Button(self.__root, text='Принять')
        btm.place(x=20, y=320, width=300, height=40)
        btm.bind('<Button-1>', self.event_btn_1)

        btm = Button(self.__root, text='Отмена')
        btm.place(x=340, y=320, width=300, height=40)
        btm.bind('<Button-1>', self.event_btn_2)

        pass

    def close(self):
        ManagerOfScreens.active_screen = SMain
        self.__root.destroy()
        pass
    
    def event_btn_1(self, event):
        self.close()
        pass
    def event_btn_2(self, event):
        
        param_add_repeat.value= self.__param_add_repeat
        param_add_best.value = self.__param_add_best
        param_size_of_selection.value = self.__param_size_of_selection
        param_generation_in_selection.value = self.__param_generation_in_selection
        param_probab_distr.value = self.__param_probab_distr 

        self.close()
        pass
    
    def event_sld_1(self, event):
        param_add_repeat.value = bool(event.value())
        pass
    def event_sld_2(self, event):
        param_add_best.value = bool(event.value())
        pass
    def event_sld_3(self, event):
        param_size_of_selection.value = event.value()
        pass
    def event_sld_4(self, event):
        param_generation_in_selection.value = event.value()
        pass
    def event_sld_5(self, event):
        param_probab_distr.value = event.value()

        list = [random_(16) for i in range(500)]

        self.__graf.clear_ranges()
        self.__graf.add_range(
                        name='range',
                        color='blue', 
                        width=5, 
                        inf=False,
                        values=[list.count(i) for i in range(15)]
                        )
            

        pass

    pass
class SSettingsOfCrossing(object):
    """Экран настройки скрещивания"""

    def __init__(self):
        
        self.__root = Tk()
        self.__root.title('Параметры скрещивания')
        self.__root.geometry('660x200')
        self.__root.resizable(width=False, height=False)
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        CenterOnScreen(self.__root, size=[660,245])
        self.__root.focus_force()
        
        self.info = WInfoBox(
                        self.__root,
                        pos=[340,20],
                        size=[300,105])
        
        min = (param_size_of_selection.value-1)
        max =  (param_size_of_chromosom.value-1)
        if min > max:
            max = min

        WSliderWithSign(
                    self.__root, 
                    pos=[20, 20], 
                    length=300, 
                    text='Тип селекции',
                    min=1, max=2, default_value=param_type_of_crossing.value,
                    event_change_value=self.event_sld_1)
        WSliderWithSign(
                    self.__root, 
                    pos=[20, 80], 
                    length=300, 
                    text='Количество точек разрыва',
                    min=min, 
                    max=max, 
                    default_value=param_count_of_breakpoints.value,
                    event_change_value=self.event_sld_2)
        
        self.__param_type_of_crossing = param_type_of_crossing.value
        self.__param_count_of_breakpoints = param_count_of_breakpoints.value

        btm = Button(self.__root, text='Принять')
        btm.place(x=20, y=140, width=300, height=40)
        btm.bind('<Button-1>', self.event_btn_1)

        btm = Button(self.__root, text='Отмена')
        btm.place(x=340, y=140, width=300, height=40)
        btm.bind('<Button-1>', self.event_btn_2)

        pass

    def close(self):
        ManagerOfScreens.active_screen = SMain
        self.__root.destroy()
        pass
    
    def event_btn_1(self, event):
        
        self.close()
        pass
    def event_btn_2(self, event):
        
        param_type_of_crossing.value = self.__param_type_of_crossing
        param_count_of_breakpoints.value = self.__param_count_of_breakpoints

        self.close()
        pass
    
    def event_sld_1(self, event):
        param_type_of_crossing.value = event.value()
        
        if event.value() == 1:
            self.info.clear_line()
            self.info.add_line('Скрещивание с фиксированным разрывом.')
        if event.value() == 2:
            self.info.clear_line()
            self.info.add_line('Попарное скрещивание с\n динамическим разрывом.')

        pass
    def event_sld_2(self, event):
        param_count_of_breakpoints.value = event.value()
        pass

    pass
class SSettingsOfEnding(object):
    """Экран настройки завершения"""

    def __init__(self):
        
        self.__root = Tk()
        self.__root.title('Условия завершения')
        self.__root.geometry('660x260')
        self.__root.resizable(width=False, height=False)
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        CenterOnScreen(self.__root, size=[660,260])
        self.__root.focus_force()


        
        WSliderWithSign(
                    self.__root, 
                    pos=[20, 20], 
                    length=300, 
                    text='Количество итераций',
                    min=0, max=5000, step=5, default_value=param_count_of_iters.value,
                    min_value='нет',
                    event_change_value=self.event_sld_1)
        WSliderWithSign(
                    self.__root, 
                    pos=[20, 80], 
                    length=300, 
                    text='Порог качества',
                    min=0, max=1, step=.01, default_value=param_min_of_quality.value,
                    min_value='нет',
                    event_change_value=self.event_sld_2)
        WSliderWithSign(
                    self.__root, 
                    pos=[20, 140], 
                    length=300, 
                    text='Итераций без роста качества',
                    min=0, max=100, default_value=param_iter_without_up.value,
                    min_value='нет',
                    event_change_value=self.event_sld_3)
        
        self.__param_count_of_iters = param_count_of_iters.value
        self.__param_min_of_quality = param_min_of_quality.value
        self.__param_iter_without_up = param_iter_without_up.value


        btm = Button(self.__root, text='Принять')
        btm.place(x=20, y=200, width=300, height=40)
        btm.bind('<Button-1>', self.event_btn_1)

        btm = Button(self.__root, text='Отмена')
        btm.place(x=340, y=200, width=300, height=40)
        btm.bind('<Button-1>', self.event_btn_2)

        pass

    def close(self):
        ManagerOfScreens.active_screen = SMain
        self.__root.destroy()
        pass
    
    def event_btn_1(self, event):
        
        self.close()
        pass
    def event_btn_2(self, event):

        param_count_of_iters.value = self.__param_count_of_iters
        param_min_of_quality.value = self.__param_min_of_quality
        param_iter_without_up.value = self.__param_iter_without_up

        self.close()
        pass
    
    def event_sld_1(self, event):
        param_count_of_iters.value = event.value()
        
        if event.value() == 1:
            self.info.clear_line()
            self.info.add_line('Скрещивание с фиксированным разрывом.')
        if event.value() == 2:
            self.info.clear_line()
            self.info.add_line('Попарное скрещивание с\n динамическим разрывом.')

        pass
    def event_sld_2(self, event):
        param_min_of_quality.value = event.value()
        pass
    def event_sld_3(self, event):
        param_iter_without_up.value = event.value()
        pass

    pass
class SSaveResult(object):
    """Экран сохранения результата"""

    def __init__(self):
        
        self.__root = Tk()
        self.__root.title('Сохранение результата')
        self.__root.geometry('340x120')
        self.__root.resizable(width=False, height=False)
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        CenterOnScreen(self.__root, size=[340,120])
        self.__root.focus_force()

        self.entry = Entry(self.__root)
        self.entry.place(x=20, y=20, width=300, height=20)

        btm = Button(self.__root, text='Принять')
        btm.place(x=20, y=60, width=140, height=40)
        btm.bind('<Button-1>', self.event_btn_1)

        btm = Button(self.__root, text='Отмена')
        btm.place(x=180, y=60, width=140, height=40)
        btm.bind('<Button-1>', self.event_btn_2)

        pass

    def close(self):
        ManagerOfScreens.active_screen = SMain
        self.__root.destroy()
        pass
    
    def event_btn_1(self, event):
        
        self.close()
        pass
    def event_btn_2(self, event):
        self.close()
        pass

    pass
class SOptionsOfResult(object):
    """Экран опций результатов"""

    def __init__(self):
        
        self.__root = Tk()
        self.__root.title('Результаты')
        self.__root.geometry('340x200')
        self.__root.resizable(width=False, height=False)
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        CenterOnScreen(self.__root, size=[340,200])
        self.__root.focus_force()

        btm = Button(self.__root, text='Просмотр результатов')
        btm.place(x=20, y=20, width=300, height=40)
        btm.bind('<Button-1>', self.event_btn_1)

        btm = Button(self.__root, text='Сравнение результатов')
        btm.place(x=20, y=70, width=300, height=40)
        btm.bind('<Button-1>', self.event_btn_2)

        btm = Button(self.__root, text='Назад')
        btm.place(x=20, y=140, width=300, height=40)
        btm.bind('<Button-1>', self.event_btn_3)

        pass

    def close(self):
        ManagerOfScreens.active_screen = SMain
        self.__root.destroy()
        pass

    def event_btn_1(self, event):
        ManagerOfScreens.active_screen = SViewResults
        self.__root.destroy()
        print('btn_1')

        pass
    def event_btn_2(self, event):
        ManagerOfScreens.active_screen = SComparisonResults
        self.__root.destroy()
        print('btn_1')

        pass
    def event_btn_3(self, event):
        self.close()
        pass

    pass
class SComparisonResults(object):
    """Экран сравнения результатов"""

    def __init__(self):
        
        self.__root = Tk()
        self.__root.title('Сравнение результатов')
        self.__root.geometry('1140x660')
        self.__root.resizable(width=False, height=False)
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        CenterOnScreen(self.__root, size=[1140,660])
        self.__root.focus_force()

        btm = Button(self.__root, text='Сохранить как')
        btm.place(x=827, y=340, width=293, height=60)
        # btm.bind('<Button-1>', self.event_btn_1)

        btm = Button(self.__root, text='Назад')
        btm.place(x=827, y=580, width=293, height=60)
        btm.bind('<Button-1>', self.event_btn_3)

        listbox = Listbox(self.__root,selectmode=SINGLE)
        listbox.place(x=20, y=340, width=360, height=300)

        listbox = Listbox(self.__root,selectmode=SINGLE)
        listbox.place(x=440, y=340, width=360, height=300)

        self.__graf = WGraph(self.__root, [20,20], [500,300])
        
        size = 11

        Label(self.__root, text='И', font='Times %i bold' % size).place(x=389, y=460, width=42, height=30)

        Label(self.__root, text='Параметры', font='Times %i bold' % size).place(x=540, y=20, width=580, height=20)
        Label(self.__root, text='Селекция', font='Times %i bold' % size).place(x=540, y=140, width=280, height=20)
        Label(self.__root, text='Скрещивание', font='Times %i bold' % size).place(x=840, y=45, width=280, height=20)
        Label(self.__root, text='Условия остановки', font='Times %i bold' % size).place(x=840, y=130, width=280, height=20)
        Label(self.__root, text='Результат', font='Times %i bold' % size).place(x=840, y=235, width=280, height=20)



        Label(self.__root, anchor='e', text='Размер хромосомы:', font='Times %i' % (size)).place(x=540, y=60, width=180, height=20)
        self.__lable_1 = Label(self.__root, text='1000/1000', font='Times %i' % (size))
        self.__lable_1.place(x=720, y=60, width=100, height=20)
        
        Label(self.__root, anchor='e', text='Размер популяции:', font='Times %i' % (size)).place(x=540, y=80, width=180, height=20)
        self.__lable_2 = Label(self.__root, text='100/100', font='Times %i' % (size))
        self.__lable_2.place(x=720, y=80, width=100, height=20)
        
        Label(self.__root, anchor='e', text='Вероятность мутации:', font='Times %i' % (size)).place(x=540, y=100, width=180, height=20)
        self.__lable_3 = Label(self.__root, text='1%/1%', font='Times %i' % (size))
        self.__lable_3.place(x=720, y=100, width=100, height=20)
        

        Label(self.__root, anchor='e', text='Распредел. вероятности:', font='Times %i' % (size)).place(x=540, y=165, width=180, height=20)
        self.__lable_4 = Label(self.__root, text='0%/0%', font='Times %i' % (size))
        self.__lable_4.place(x=720, y=165, width=100, height=20)
        
        Label(self.__root, anchor='e', text='Повторения в отборе:', font='Times %i' % (size)).place(x=540, y=185, width=180, height=20)
        self.__lable_5 = Label(self.__root, text='нет/нет', font='Times %i' % (size))
        self.__lable_5.place(x=720, y=185, width=100, height=20)
        
        Label(self.__root, anchor='e', text='Учет лучшего:', font='Times %i' % (size)).place(x=540, y=205, width=180, height=20)
        self.__lable_6 = Label(self.__root, text='нет/нет', font='Times %i' % (size))
        self.__lable_6.place(x=720, y=205, width=100, height=20)
        
        Label(self.__root, anchor='e', text='Размер отбора:', font='Times %i' % (size)).place(x=540, y=225, width=180, height=20)
        self.__lable_7 = Label(self.__root, text='2/2', font='Times %i' % (size))
        self.__lable_7.place(x=720, y=225, width=100, height=20)
        
        Label(self.__root, anchor='e', text='Поколений в отборе:', font='Times %i' % (size)).place(x=540, y=245, width=180, height=20)
        self.__lable_8 = Label(self.__root, text='1/1', font='Times %i' % (size))
        self.__lable_8.place(x=720, y=245, width=100, height=20)
        

        Label(self.__root, anchor='e', text='Тип:', font='Times %i' % (size)).place(x=840, y=70, width=180, height=20)
        self.__lable_9 = Label(self.__root, text='1/2', font='Times %i' % (size))
        self.__lable_9.place(x=1020, y=70, width=100, height=20)

        Label(self.__root, anchor='e', text='Кол-во точек разрыва:', font='Times %i' % (size)).place(x=840, y=90, width=180, height=20)
        self.__lable_10 = Label(self.__root, text='1/1', font='Times %i' % (size))
        self.__lable_10.place(x=1020, y=90, width=100, height=20)
        

        Label(self.__root, anchor='e', text='Количество итераций:', font='Times %i' % (size)).place(x=840, y=155, width=180, height=20)
        self.__lable_11 = Label(self.__root, text='5000/5000', font='Times %i' % (size))
        self.__lable_11.place(x=1020, y=155, width=100, height=20)

        Label(self.__root, anchor='e', text='Порог качества:', font='Times %i' % (size)).place(x=840, y=175, width=180, height=20)
        self.__lable_12 = Label(self.__root, text='90%/90%', font='Times %i' % (size))
        self.__lable_12.place(x=1020, y=175, width=100, height=20)

        Label(self.__root, anchor='e', text='Итераций без роста:', font='Times %i' % (size)).place(x=840, y=195, width=180, height=20)
        self.__lable_13 = Label(self.__root, text='100/100', font='Times %i' % (size))
        self.__lable_13.place(x=1020, y=195, width=100, height=20)
        

        Label(self.__root, anchor='e', text='Количество итераций:', font='Times %i' % (size)).place(x=840, y=260, width=180, height=20)
        self.__lable_14 = Label(self.__root, text='311/512', font='Times %i' % (size))
        self.__lable_14.place(x=1020, y=260, width=100, height=20)

        Label(self.__root, anchor='e', text='Качество:', font='Times %i' % (size)).place(x=840, y=280, width=180, height=20)
        self.__lable_15 = Label(self.__root, text='91%/92%', font='Times %i' % (size))
        self.__lable_15.place(x=1020, y=280, width=100, height=20)
        
        pass

    def close(self):
        ManagerOfScreens.active_screen = SOptionsOfResult
        self.__root.destroy()
        pass


    def event_btn_3(self, event):
        self.close()
        pass

    pass
class SViewResults(object):
    """Экран просмотра результатов"""

    def __init__(self):
        
        self.__root = Tk()
        self.__root.title('Просмотр результатов')
        self.__root.geometry('1000x660')
        self.__root.resizable(width=False, height=False)

        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        CenterOnScreen(self.__root, size=[1000,660])
        self.__root.focus_force()

        btm = Button(self.__root, text='Удалить')
        btm.place(x=400, y=20, width=160, height=60)
        # btm.bind('<Button-1>', self.event_btn_1)

        btm = Button(self.__root, text='Отчистить')
        btm.place(x=400, y=85, width=160, height=60)
        # btm.bind('<Button-1>', self.event_btn_1)

        btm = Button(self.__root, text='Назад')
        btm.place(x=400, y=225, width=160, height=60)
        btm.bind('<Button-1>', self.event_btn_3)

        listbox = Listbox(self.__root,selectmode=SINGLE)
        listbox.place(x=20, y=20, width=360, height=620)
        
        for i in range(100):
            listbox.insert(END,i)

        
        self.__graf = WGraph(self.__root, [580,20], [400,265])

        pass

    def close(self):
        ManagerOfScreens.active_screen = SOptionsOfResult
        self.__root.destroy()
        pass


    def event_btn_3(self, event):
        self.close()
        pass

    pass

class ManagerOfScreens(object):
    """Менеджер окон

    Запускает необходимые для продолжения работы окна.
    
    """

    active_screen:'Активное окно' = SMain

    def start():
        """Запуск работы менеджера"""
        while(not is_end_run_app['value']):
            ManagerOfScreens.active_screen()
            mainloop()
        pass


    pass

def CenterOnScreen(root, size=[0,0]):
    """Метод центровки окна"""
    
    x = (root.winfo_screenwidth() - size[0]) / 2
    y = (root.winfo_screenheight() - size[1]) / 2
    root.geometry("+%d+%d" % (x, y))

    pass


def WithOutGUI():


    INFO('start GA')

    q = []

    
    print ('Необходимо задать параметры сессии')
    print ('Кол-во итераций для усреднения значений [1, 30]: ')
    count = int(input())
    
    # блок общих параметров ГА
    print ('Размер хромосомы [2, 100]: ')
    param_size_of_chromosom.value = int(input())
    print ('Размер популяции [2, 25]: ')
    param_size_of_population.value = int(input())
    print ('Вероятность мутации [0.0, 1.0]: ')
    param_chance_of_mutation.value = float(input())

    # блок общих параметров ГА-селекции
    print ('Распределение вероятности [0.0, 1.0]: ')
    param_probab_distr.value = float(input())
    print ('Повторения в отборе [0, 1]: ')
    param_add_repeat.value = bool(input())
    print ('Учет лучшего [0, 1]: ')
    param_add_best.value = bool(input())
    print ('Размер отбора [2, 25]: ')
    param_size_of_selection.value = int(input())
    print ('Поколений в отборе [1, 5]: ')
    param_generation_in_selection.value = int(input())
        
    # блок общих параметров ГА-скрещивания
    print ('Тип скрещивания [1, 2]: ')
    param_type_of_crossing.value = int(input())
    print ('Количество точек разрыва [1, 99]: ')
    param_count_of_breakpoints.value = int(input())
    
    # блок общих параметров ГА-остановки 
    print ('Количество итераций для остановки [0, 1000]: ')
    param_count_of_iters.value = int(input())
    print ('Порог качества для остановки [0.0, 1.0]: ')
    param_min_of_quality.value = float(input())
    print ('Итерация без роста для остановки [1, 1000]: ')
    param_iter_without_up.value = int(input())

    for i in range(count):
        print('iter ', i)

        ga = GA()

        ga.generation_person = generation_person
        ga.selection = selection
        ga.crossing = crossing
        ga.mutation = mutation
        ga.def_quality = definition_quality
        ga.is_end = end

        ga.preparing()

        qualities = [ga.the_best_person_of_population.quality]
        theBestes = [list(ga.the_best_person_of_population.get_chromo())]

        iter = 1

        while not ga.iteration(): 
            qualities.append(ga.the_best_person_of_population.quality)
            theBestes.append(list(ga.the_best_person_of_population.get_chromo()))
            iter += 1

        q.append(qualities)

    SaveExcelResultReport(q)

    pass

def main():

    
    
    pass

if __name__ == '__main__': main()