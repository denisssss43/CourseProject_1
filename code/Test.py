from genetic_algorithm import *
import math
import random
import Main
import tkinter as tk
import threading
import param

random.seed()


s_chrom = 30
param.param_size_of_population.value = 45
s_select = 2
c_bp = 1

ch_mutation = .015


def GenerationPerson(self=GA()):
    
    size        = s_chrom-2
    inPIndex    = 0
    outPIndex   = 1

    person = Person()
    chromo = [inPIndex]
    for index in range(size):
        valid = [i for i in range(len(points)) if chromo.count(i) == 0 and i != outPIndex]
        chromo.append(valid[random.randint(0, len(valid)-1)])
    chromo.append(outPIndex)
    person.add_chromo(list(chromo))
    
    self.last_population.append(person)
    
    pass
def DefinitionQuality(self=GA()):

    for person in self.last_population:
        chromo = person.chromos[0]
        quality = 0

        for i in [ i for i in range(len(person.chromos[0])-1)]:
            p1 = points[person.chromos[0][i]]
            p2 = points[person.chromos[0][i+1]]
            quality += math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) 
        if quality == 0: person.quality =  quality
        else: person.quality =  float(q_best/quality)

    pass
def Selection(self=GA()):
    size = 2
    selected = [] 

    while len(selected) < s_select: 
        selected.append(
            Person(
                self.last_population[Main.random_(len(self.last_population), .85)]
                )
        )

    self.last_selected = selected
    pass
def Crossing(self=GA()):
    
    # print(self.last_selected[0].chromos)

    chromo = list(self.last_selected[0].chromos[0])

    self.last_selected.sort(reverse=False)

    validBPPos = [i for i in  range(s_chrom-1)]
    breakpoints = []

    for i in range(c_bp):  # Генерация точек разрыва
        randIndex = random.randint(0,len(validBPPos)-1)
        breakpoints.append(validBPPos[randIndex])
        validBPPos.pop(randIndex)

    breakpoints.sort()

    index_gene = 0  # Индекс гена
    index_pers = 0  # Индекс особи
    index_bp = 0    # Индекс точки разрыва
    
    chromo = []
    
    while index_gene < s_chrom:
        
        if breakpoints[index_bp] < index_gene:  # Проверка достижения точки разрыва
            index_bp += 1
            index_pers += 1

        if index_pers >= len(self.last_selected):  # Сброс индекса особи
            index_pers = 0

        if index_bp >= c_bp:  # Проверка исчерпания списка точек селекции
            pers = Person(self.last_selected[index_pers])
            chromo.extend(pers.get_chromo(0)[breakpoints[index_bp-1]+1:])
            break

        pers = Person(self.last_selected[index_pers])
        chromo.append(pers.get_chromo(0)[index_gene])
        
        index_gene += 1

    for i in range(len(chromo)):  # Нормализация
        valid = [i for i in range(len(chromo)) if chromo.count(i) == 0]
        if chromo.count(chromo[i]) > 1: chromo[i] = valid[random.randint(0, len(valid)-1)]

    self.last_crossed = Person()
    self.last_crossed.add_chromo(chromo)

    pass
def Mutation(self=GA()):

    mutated = Person()
    chr = self.last_crossed.chromos[0]



    for i in [q+1 for q in range(len(chr)-2)]:
        if ch_mutation > random.random():
            num = random.randint(1,len(chr)-2)
            gene = chr[i]
            chr[i] = chr[num]
            chr[num] = gene

    if ch_mutation > random.random():
        chr_1 = chr[1:-1]
        chr_1.reverse()
        chr_1 = chr[:1] + chr_1 + chr[-1:]
        chr = chr_1

    mutated.add_chromo(list(chr))

    self.last_mutated = mutated

    return 

    mutated = Person()
    chr = []

    chr += self.last_crossed.chromos[0][:1]
    for gene in self.last_crossed.chromos[0][1:-1]:
        if ch_mutation > random.random():
           valid = [i for i in range(len(points)) if chr.count(i) == 0 and i != self.last_crossed.chromos[0][-1:]]
           chr.append(valid[random.randint(0, len(valid)-1)])
        else: chr.append(gene)
    chr += self.last_crossed.chromos[0][-1:]

    for i in range(len(chr)):
        valid = [i for i in range(len(chr)) if chr.count(i) == 0]
        if chr.count(chr[i]) > 1: chr[i] = valid[random.randint(0, len(valid)-1)]

    mutated.add_chromo(list(chr))

    self.last_mutated = mutated
    pass
def End(self=GA()):
    print(len(self.past_population),'iter', self.the_best_person_of_population.quality)
    return len(self.past_population) >= 2000


ga = GA()
ga.generation_person = GenerationPerson
ga.def_quality = DefinitionQuality
ga.selection = Selection
ga.crossing = Crossing
ga.mutation = Mutation
ga.is_end = End

# points = [(.5*math.sin(i*2*math.pi/s_chrom)+1, .5*math.cos(i*2*math.pi/s_chrom)+1) for i in range(s_chrom)]
points = [(random.random()+.5, random.random()+.5) for i in range(s_chrom)]
best = [i for i in range(s_chrom)]
q_best = 0
for i in [ i for i in range(len(best)-1)]:
    p1 = points[best[i]]
    p2 = points[best[i+1]]
    q_best += math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

color_1 = 'black'
color_2 = 'white'
color_3 = 'gray'


ga.preparing()

iter = 0
def update():
    
    while True:
        
        global iter
        iter+=1

        global ga
        isEnd = ga.iteration()

        
        canv.delete('all')

        canv.create_text(25, 25, text=('iter: ' + str(iter)), font="Consolas 12",anchor="w", fill=color_2)
        canv.create_text(25, 50, text=('mCh: ' + str(ch_mutation*100)) + '%', font="Consolas 12",anchor="w", fill=color_2)
        canv.create_text(25, 75, text=('pCount: ' + str(s_chrom)), font="Consolas 12",anchor="w", fill=color_2)
        canv.create_text(25, 100, text=('pSize: ' + str(param.param_size_of_population.value)), font="Consolas 12",anchor="w", fill=color_2)

        for i in [ i for i in range(len(ga.the_best_person_of_population.chromos[0])-1)]:
            p1 = points[ ga.the_best_person_of_population.chromos[0][i]]
            p2 = points[ ga.the_best_person_of_population.chromos[0][i+1]]
            canv.create_line(p1[0]*300,p1[1]*300,p2[0]*300,p2[1]*300, width=2, fill=color_1) 
            canv.create_line(p1[0]*300,p1[1]*300,p2[0]*300,p2[1]*300, width=1, fill=color_3)
            
        for i in [ i for i in range(len(ga.the_best_person.chromos[0])-1)]:
            p1 = points[ ga.the_best_person.chromos[0][i]]
            p2 = points[ ga.the_best_person.chromos[0][i+1]]
            canv.create_line(p1[0]*300,p1[1]*300,p2[0]*300,p2[1]*300, width=10, fill=color_1) 
            canv.create_line(p1[0]*300,p1[1]*300,p2[0]*300,p2[1]*300, width=4, fill=color_2) 

        if isEnd: return
        # canv.after(1, update)

    pass


root = tk.Tk()
canv = tk.Canvas(root, width=600, height=600, bg = color_1)
canv.pack()
btn = tk.Button(root, text = '...')
btn.bind('<Button-1>', lambda event: threading.Thread(target=update, daemon=True).start())
canv.pack()
btn.pack()
root.mainloop()

