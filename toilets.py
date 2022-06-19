import matplotlib.pyplot as plt
import numpy as np
import toilets_2 as toilets_2
import pprint

class person_class:
    def __init__(self, piss_chance, poop_chance, vomit_chance, sex_chance):
        self.sex = self.what_sex(np.random.rand(), sex_chance)
        self.need = self.what_need(np.random.rand(),  piss_chance, poop_chance, vomit_chance)
        self.time = self.how_much_time(self.need, self.sex, times)
        self.jointime = None
        self.lefttime = None

    def what_sex(self, random, sex_chance):
        if random > sex_chance:
            return "Male"
        else:
            return "Female"

    def what_need(self, random, piss_chance, poop_chance, vomit_chance):
        if random <= piss_chance:
            return 'piss'
        elif random > piss_chance and random < (piss_chance + poop_chance):
            return 'poop'
        elif random > (piss_chance + poop_chance) and random < (piss_chance + poop_chance + vomit_chance):
            return 'vomit'

    def how_much_time(self, what_need, sex, times):
        time = 0
        if sex == 'Female':
            if what_need == 'piss':
                time = np.random.randint(times['women']['piss'][0], times['women']['piss'][1])
            elif what_need == 'poop':
                time = np.random.randint(times['women']['poop'][0], times['women']['poop'][1])
            elif what_need == 'vomit':
                time = np.random.randint(times['women']['vomit'][0], times['women']['vomit'][1])

        if sex == 'Male':
            if what_need == 'piss':
                time = np.random.randint(times['men']['piss'][0], times['men']['piss'][1])
            elif what_need == 'poop':
                time = np.random.randint(times['men']['poop'][0], times['men']['poop'][1])
            elif what_need == 'vomit':
                time = np.random.randint(times['men']['vomit'][0], times['men']['vomit'][1])
        return time

class men_toilet_class:
    def __init__(self, urinal_number, toilet_number):
        self.urinals = [[] for i in range(urinal_number)]
        self.toilets = [[] for i in range(toilet_number)]
        self.queue = []
        self.stats = []

    def queue_add(self, person):
        self.queue.append(person)

    def toilet_operations(self, actuall_time):
        #korzystanie z toalety
        for toilet in self.toilets:
            if not toilet:
                try:
                    toilet.append(self.queue[0])
                    toilet[0].lefttime = actuall_time
                    del self.queue[0]
                except: pass
            else:
                toilet[0].time -= 1
                if toilet[0].time == 0:
                    self.stats.append(toilet[0])
                    del toilet[0]

        #korzystanie z pisuaru
        for urinal in self.urinals:
            if not urinal:
                for i in range(len(self.queue)):
                    if self.queue[i].need == 'piss':
                        urinal.append(self.queue[i])
                        urinal[0].lefttime = actuall_time
                        del self.queue[i]
                        break
            else:
                urinal[0].time -= 1
                if urinal[0].time == 0:
                    self.stats.append(urinal[0])
                    del urinal[0]

class women_toilet_class:
    def __init__(self, toilet_number):
        self.toilets = [[] for i in range(toilet_number)]
        self.queue = []
        self.stats = []

    def queue_add(self, person):
        self.queue.append(person)

    def toilet_operations(self, actuall_time):
        for toilet in self.toilets:
            if not toilet:
                try:
                    toilet.append(self.queue[0])
                    toilet[0].lefttime = actuall_time
                    del self.queue[0]
                except: pass
            else:
                toilet[0].time -= 1
                if toilet[0].time == 0:
                    self.stats.append(toilet[0])
                    del toilet[0]


def witch_toilet(person, women_toilet, men_toilet, time):
    if person.sex == 'Female':
        women_toilet.queue_add(person)
    else:
        men_toilet.queue_add(person)
    person.jointime = time


def simulation_2_toilets(time_in_secounds, sim_num):
        #parametry symulacji
    actuall_time = 0
        #towrzenie toalet
    men_toilet = men_toilet_class(men_toilet_structur['urinal'], men_toilet_structur['toilet'])
    women_toilet = women_toilet_class(women_toilet_structur['toilet'])

    while time_in_secounds != actuall_time:
        if np.random.rand() <= new_chance:
            witch_toilet(person_class(piss_chance, poop_chance, vomit_chance, sex_chance),
                         women_toilet,
                         men_toilet,
                         actuall_time)
            #dzialania w toaletach
        women_toilet.toilet_operations(actuall_time)
        men_toilet.toilet_operations(actuall_time)

            #dodanie jednej sekudny do aktualnego czasu symulacji
        actuall_time += 1

    all_times_in_men_toilet = []
    for person in men_toilet.stats:
        all_times_in_men_toilet.append(person.lefttime - person.jointime)
    all_times_in_women_toilet = []
    for person in women_toilet.stats:
        all_times_in_women_toilet.append(person.lefttime - person.jointime)

    return round((round(np.mean(all_times_in_men_toilet), 0) * len(men_toilet.stats) +
            round(np.mean(all_times_in_women_toilet)) * len(women_toilet.stats))/
            (len(women_toilet.stats) + len(men_toilet.stats)), 0)

#3 poziomy:
new_to_toilet_chance_all = [0.16, 0.18, 0.20]
female_chance = [0.5, 0.63, 0.75]

all_sim_data = []
file = open('toilets_data.txt', 'w')
jakaszmienna = 0
for new_chance in new_to_toilet_chance_all:
    for sex_chance in female_chance:

        #parametry symuacji
        ile_godzin = 8
        piss_chance = 0.93
        poop_chance = 0.02
        vomit_chance = 0.05
        new_to_toilet_chance = new_chance
        men_toilet_structur = {'urinal': 3,
                               'toilet': 1}
        women_toilet_structur = {'toilet': 4}

        #czas potrzeby
        times = {'women': {'piss': [30, 50],
                           'poop': [50, 80],
                           'vomit': [30,50]},
                 'men': {'piss': [30, 40],
                         'poop': [60, 120],
                         'vomit': [30,50]}}

        #wywolanie symulacji
        ile_razy = 40

        sim_data = []
        file.write('| %s, %s |\n'%(new_chance, sex_chance))
        for i in range(ile_razy):
            print(i + ile_razy * jakaszmienna, '/', ile_razy * 9, 'osobne')
            sim = simulation_2_toilets(ile_godzin * 60 * 60, i)
            file.write('\t%s: %s\n'%(i, sim))
            sim_data.append(sim)
        all_sim_data.append(sim_data)
        jakaszmienna += 1

def mean_for_new_chance():
    list = []
    for i in range(3):
        list.append(
            np.mean(
                [np.mean(all_sim_data[i]),
                 np.mean(all_sim_data[i + 3]),
                 np.mean(all_sim_data[i + 6])]))
    return list

def mean_for_female_chance():
    list = []
    for i in range(3):
        list.append(
            np.mean(
                [np.mean(all_sim_data[0 + i * 3]),
                 np.mean(all_sim_data[1 + i * 3]),
                 np.mean(all_sim_data[2 + i * 3])]))
    return list

def wykres(x_axis, y_axis1, y_axis2, x_title):
    plt.plot(x_axis,
             y_axis1,
             'r-o',
             label = "oddzielne toalety",
             color = 'blue')
    plt.plot(x_axis,
             y_axis2,
             'r-o',
             label = "koedukacyjna toaleta",
             color = 'red')
    plt.xticks(x_axis, rotation = 0)
    plt.xlabel(x_title)
    plt.ylabel('Mean time in queue')
    plt.legend()
    plt.grid()

plt.rcParams["figure.figsize"] = (10, 10)
plt.subplot(2,1,1)
wykres(new_to_toilet_chance_all, mean_for_new_chance(), toilets_2.mean_for_new_chance(), "New in toilet chance")
plt.subplot(2,1,2)
wykres(female_chance, mean_for_female_chance(), toilets_2.mean_for_female_chance(), "Female chance")
plt.show()

toilets_data = []
plt.rcParams["figure.figsize"] = (5, 5)
for i in range(len(all_sim_data)):
    toilets_data += all_sim_data[i]

filepy = open("dtoilets.py", 'w')
filepy.write('all_sim_data = ' + pprint.pformat(all_sim_data, width = 100, compact = True))
filepy.write('\nall_sim_data2 = ' + pprint.pformat(toilets_2.all_sim_data, width = 100, compact = True))

plt.boxplot([toilets_data, toilets_2.toilets_data], labels = ['osobne', 'koedukacyjne'])
plt.ylabel('Time in queue')
plt.grid()
plt.show()














