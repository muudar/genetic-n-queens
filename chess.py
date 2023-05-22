import random
import numpy as np
from flask import Flask, render_template, request


app = Flask(__name__)

def get_fitness(chromosome):
    n = len(chromosome)
    fitness = (n-1) * (n) / 2
    for i in range(n):
        for j in range(i+1, n):
            if chromosome[i] == chromosome[j]:
                fitness -= 1
            if abs(chromosome[i] - chromosome[j]) == j - i:
                fitness -= 1
    return fitness

def total_fitness(population):
    total = 0
    for i in range(len(population)):
        total += get_fitness(population[i])
    return total

def fitness_vals(population):
    vals = []
    for i in range(len(population)):
        value = get_fitness(population[i])
        vals.append(value)
    return vals


def get_probabilities(population):
    probabilities = []
    fitness_sum = total_fitness(population)
    for i in range(len(population)):
        probabilities.append(get_fitness(population[i]) / fitness_sum)
    return probabilities


def select_population(population):
    if len(population) % 2 == 1:
        population.pop()
    probabilities = get_probabilities(population)
    indices = list(range(len(population)))
    selected_indicies = np.random.choice(indices, size = len(population), p = probabilities)
    selected_population = []
    for i in range(len(selected_indicies)):
        selected_population.append(population[selected_indicies[i]])
    return selected_population 




def generate_chromosome(boardSize):
    arr = list(range(boardSize))
    random.shuffle(arr)
    return arr

def generate_initial_population(N, boardSize):
    arr = []
    for i in range(N):
        arr.append(generate_chromosome(boardSize))
    return arr


def crossover(N,parent1, parent2, crossover_probability):
    random_probability = np.random.random()
    if crossover_probability > random_probability:
        random_index = np.random.randint(1,N)
        child1 = parent1[:random_index] + parent2[random_index:]
        child2 = parent1[random_index:] + parent2[:random_index]
    else:
        child1 = parent1.copy()
        child2 = parent2.copy()
    return child1, child2

def mutation(N,chromosome, mutation_probability):
    random_probability = np.random.random()
    if mutation_probability > random_probability:
        random_index = np.random.randint(N)
        chromosome[random_index] = np.random.randint(N)
    return chromosome

def crossover_and_mutation(N,selected_population, crossover_probability, mutation_probability):
    population_length = len(selected_population)
    new_generation = []
    for i in range(0, population_length, 2):
        parent1 = selected_population[i]
        parent2 = selected_population[i+1]
        child1, child2 = crossover(N,parent1, parent2, crossover_probability)
        new_generation.append(child1)
        new_generation.append(child2)
    for i in range(len(new_generation)):
        mutation(N,new_generation[i], mutation_probability)
    return new_generation 


def solution(board_size, population_size, crossover_probability, mutation_probability, max_gen):
    population = generate_initial_population(population_size, board_size)
    max_fitness = (board_size - 1) * board_size / 2
    best_fitness = None
    current_gen = 0
    while(True):
        fitness_values = fitness_vals(population)
        best_fitness = max(fitness_values)
        if(best_fitness == max_fitness):
            best_index = fitness_values.index(best_fitness)
            print("Found a solution in generation " + str(current_gen))
            print(population[best_index])
            return {
                'best': population[best_index],
                'gen': current_gen,
                'solved' : True
            }
        elif(current_gen == max_gen):
            best_solution = max(fitness_values)
            best_solution_index = fitness_values.index(best_solution)
            return {
                'best': population[best_solution_index],
                'gen': current_gen,
                'solved' : False
            }
        else:
            selected_population = select_population(population)
            population = crossover_and_mutation(board_size,selected_population, crossover_probability , mutation_probability)
            current_gen+=1
                

    
@app.route('/solution', methods=['GET', 'POST'])
def displaySolution():
    if request.method == 'POST':
        board_size = request.form['board-size']
        initial_population = request.form['initial-population']
        mutation_probability = request.form['mutation-probability']
        crossover_probability = request.form['crossover-probability']
        max_gen = request.form['max-number-of-gen']
        sol = solution(int(board_size),int(initial_population),float(crossover_probability),float(mutation_probability), int(max_gen))
        return render_template('solution.html', solArray = sol['best'], n = board_size, gen = sol['gen'], solved = sol['solved'])

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
