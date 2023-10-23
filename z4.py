import time

import pygad
import numpy

L = [[1,1,1,1,1,1,1,1,1,1,1,1],
     [1,'S',0,0,1,0,0,0,1,0,0,1],
     [1,1,1,0,0,0,1,0,1,1,0,1],
     [1,0,0,0,1,0,1,0,0,0,0,1],
     [1,0,1,0,1,1,0,0,1,1,0,1],
     [1,0,0,1,1,0,0,0,1,0,0,1],
     [1,0,0,0,0,0,1,0,0,0,1,1],
     [1,0,1,0,0,1,1,0,1,0,0,1],
     [1,0,1,1,1,0,0,0,1,1,0,1],
     [1,0,1,0,1,1,0,1,0,1,0,1],
     [1,0,1,0,0,0,0,0,0,0,'E',1],
     [1,1,1,1,1,1,1,1,1,1,1,1]]

def find_start_and_exit(M):
    S = []
    E = []
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] == 'S':
                S = [i, j]
            if M[i][j] == 'E':
                E = [i, j]
    if S and E == []:
        print("No start or exit")
        return 0
    return S, E


S, E = find_start_and_exit(L)

#definiujemy parametry chromosomu
#geny to liczby: 0-lewo 1-gora 2-prawo 3-dol
gene_space = [0, 1, 2, 3]

#definiujemy funkcję fitness
def fitness_func(ga_instance, solution, solution_idx):
    actual_position = S.copy()
    i = 0
    for item in solution:
        i += 1
        match item:
            case 0:
                actual_position[1] = actual_position[1] - 1
            case 1:
                actual_position[0] = actual_position[0] - 1
            case 2:
                actual_position[1] = actual_position[1] + 1
            case 3:
                actual_position[0] = actual_position[0] + 1
        if L[actual_position[0]][actual_position[1]] == 1:
            match item:
                case 0:
                    actual_position[1] = actual_position[1] + 1
                case 1:
                    actual_position[0] = actual_position[0] + 1
                case 2:
                    actual_position[1] = actual_position[1] - 1
                case 3:
                    actual_position[0] = actual_position[0] - 1
        if actual_position == E:
            return -i + 100
    fitness = -(abs(actual_position[0] - E[0]) + abs(actual_position[1] - E[1]))

    return fitness

fitness_function = fitness_func

#ile chromsomów w populacji
#ile genow ma chromosom
sol_per_pop = 10
num_genes = 30

#ile wylaniamy rodzicow do "rozmanazania" (okolo 50% populacji)
#ile pokolen
#ilu rodzicow zachowac (kilka procent)
num_parents_mating = 5
num_generations = 3000
keep_parents = 2

#jaki typ selekcji rodzicow?
#sss = steady, rws=roulette, rank = rankingowa, tournament = turniejowa
parent_selection_type = "sss"

#w il =u punktach robic krzyzowanie?
crossover_type = "single_point"

#mutacja ma dzialac na ilu procent genow?
#trzeba pamietac ile genow ma chromosom
mutation_type = "random"
mutation_percent_genes = 5
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
                           stop_criteria=["reach_30"])

    #uruchomienie algorytmu
    ga_instance.run()
    end = time.time()
    times.append(end - start)

#podsumowanie: najlepsze znalezione rozwiazanie (chromosom+ocena)
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))


print("Średnia czasów: " + str(numpy.average(times)))

#wyswietlenie wykresu: jak zmieniala sie ocena na przestrzeni pokolen
ga_instance.plot_fitness()