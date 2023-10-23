import pygad
import numpy
import time

przedmiot = ["zegar", "obraz-pejzaż", "obraz-portret", "radio", "laptop", "lampka nocna", "srebne sztućce", "porcelana", "figura z brązu", "skórzana torebka", "odkurzacz"]
waga = [7, 7, 6, 2, 5, 6, 1, 3, 10, 3, 15]
wartosc = [100, 300, 200, 40, 500, 70, 100, 250, 300, 280, 300]

#definiujemy parametry chromosomu
#geny to liczby: 0 lub 1
gene_space = [0, 1]

#definiujemy funkcję fitness
def fitness_func(ga_instance, solution, solution_idx):
    sum1 = numpy.sum(solution * wartosc)
    sum2 = numpy.sum(solution * waga)
    if sum2 > 25:
        return 0
    fitness = sum1
    #lub: fitness = 1.0 / (1.0 + numpy.abs(sum1-sum2))
    return fitness

fitness_function = fitness_func

#ile chromsomów w populacji
#ile genow ma chromosom
sol_per_pop = 10
num_genes = len(waga)

#ile wylaniamy rodzicow do "rozmanazania" (okolo 50% populacji)
#ile pokolen
#ilu rodzicow zachowac (kilka procent)
num_parents_mating = 5
num_generations = 50
keep_parents = 2

#jaki typ selekcji rodzicow?
#sss = steady, rws=roulette, rank = rankingowa, tournament = turniejowa
parent_selection_type = "sss"

#w il =u punktach robic krzyzowanie?
crossover_type = "single_point"

#mutacja ma dzialac na ilu procent genow?
#trzeba pamietac ile genow ma chromosom
mutation_type = "random"
mutation_percent_genes = 8

#start pomiaru
times = []
for i in range(10):
    start = time.time()
    #inicjacja algorytmu z powyzszymi parametrami wpisanymi w atrybuty
    ga_instance = pygad.GA(gene_space=gene_space,
                           num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes,
                           stop_criteria=["reach_1630"])

    #uruchomienie algorytmu
    ga_instance.run()
    end = time.time()
    times.append(end-start)





#podsumowanie: najlepsze znalezione rozwiazanie (chromosom+ocena)
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

#tutaj dodatkowo wyswietlamy sume wskazana przez jedynki
prediction = numpy.sum(wartosc*solution)
print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

print(f"Number of generations passed is {ga_instance.generations_completed}")

#nazwy przedmiotów
names = []
c = 0
for item in solution:

    if item == 1:
        names.append(przedmiot[c])
    c += 1
print("Best items: ")
print(names)

print("Średnia czasów: " + str(numpy.average(times)))

#wyswietlenie wykresu: jak zmieniala sie ocena na przestrzeni pokolen
ga_instance.plot_fitness()