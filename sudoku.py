import random
import time
from copy import deepcopy

import numpy as np

random.seed()

candidates = []
best_pop = []
remaining = [_ for _ in range(1, 10)]
pop_size = 10
generations = 100
mutation_rate = 0.85

# selection_rate = 0.85


"""
a test puzzle: 

    316!578!49.
    529!134!768
    487!629!531
    ---!---!---
    263!415!987
    974!8.3!125
    851!792!643
    ---!---!---
    .38!9.7!25.
    692!.51!87.
    7.5!286!31.
    
"""


def load(file):
    """

    Parameters: file - a file to load
    Returns: values - an array with the given values

    """

    f = open(file, "r")
    new = []
    for x in f:
        new.append(x.split("!"))
    p = []
    f.close()
    for m in new:
        for k in m:
            z = k.strip('\n')
            if z == '---' or z == ['---']:
                continue
            else:
                p.append(z)
    sudoku = []
    for n in range(len(p)):
        for a in p[n]:
            if a == '.':
                a = '0'
            sudoku.append(int(a))
    values = np.array(sudoku).reshape(9, 9)
    return values


startTime = time.time()

values = load('Grid1.ss')  # CHANGE GRID HERE TO TEST
given = load('Grid1.ss')  # CHANGE GRID HERE TO TEST

given_indices = [[] for i in range(0, 9)]
for x in range(0, len(given)):
    for g in range(0, len(given[x])):
        if given[x][g] != 0:
            given_indices[x].append(g)


def find_remaining(row):
    """

    Parameters: row - a row in the board
    Returns: unused - an array of unused values in row

    """
    unused = []
    for x in range(0, len(row)):
        if remaining[x] not in row:
            unused.append(remaining[x])
    return unused


"""

The following 3 functions are used to check if there are any duplicates in the row, column or 3x3 subgrid. 
They all return the amount of duplicates. 

"""


def row_duplicate(board):
    row_count = 0
    for y in board:
        if not len(np.unique(y)) == len(y):
            row_count += (9 - len(np.unique(y))) + 1
    return row_count


def col_duplicate(board):
    col_count = 0
    for y in board.T:
        if not len(np.unique(y)) == len(y):
            col_count += (9 - len(np.unique(y))) + 1
    return col_count


def squ_duplicate(board):
    new_board = []
    squares = []
    count = 0
    for x in range(0, 9, 3):
        new_board.append(board[x:x + 3])

    squares.append((new_board[0][0][0:3], new_board[0][1][0:3], new_board[0][2][0:3]))
    squares.append((new_board[0][0][3:6], new_board[0][1][3:6], new_board[0][2][3:6]))
    squares.append((new_board[0][0][6:9], new_board[0][1][6:9], new_board[0][2][6:9]))

    squares.append((new_board[1][0][0:3], new_board[1][1][0:3], new_board[1][2][0:3]))
    squares.append((new_board[1][0][3:6], new_board[1][1][3:6], new_board[1][2][3:6]))
    squares.append((new_board[1][0][6:9], new_board[1][1][6:9], new_board[1][2][6:9]))

    squares.append((new_board[2][0][0:3], new_board[2][1][0:3], new_board[2][2][0:3]))
    squares.append((new_board[2][0][3:6], new_board[2][1][3:6], new_board[2][2][3:6]))
    squares.append((new_board[2][0][6:9], new_board[2][1][6:9], new_board[2][2][6:9]))

    for y in range(0, 9):
        if not len(np.unique(np.array(squares[y]))) == 9:
            count += (9 - len(np.unique(np.array(squares[y])))) + 1
    return count


print("Seeding....")


def seed():
    """
    Returns: pop - populated grid
    """
    pop = deepcopy(values)
    for i in pop:
        for j in i:
            if j == 0:
                for x in np.where(i == 0):
                    for n in x:
                        i[n] = random.randint(1, 9)
                        if not np.unique(i.all()):
                            i[np.where(i == j)] = random.randint(1, 9)
            else:
                continue

    return pop


def fitness(board) -> float:
    """
    Parameters: board - a populated grid
    Returns: fitness - the fitness for the given board
    """
    if row_duplicate(board) + col_duplicate(board) + squ_duplicate(board) == 0:
        fitness = 0
    else:
        fitness = (col_duplicate(board) + squ_duplicate(board) + row_duplicate(board)) / 81
    return round(fitness, 6)


def population(pop_size):
    """
    Parameters: pop_size(int) - amount of individuals (candidates)
    """
    for candidate in range(0, pop_size):
        pop = deepcopy(seed())
        candidates.append((fitness(pop), pop))


population(pop_size)


def sort_pop(array):
    """
    Parameters: array - an array containing tuples to sort
    Returns: array - returns the sorted array by the fitness, from lowest to highest fitness
    """
    array.sort(key=lambda tup: tup[0])
    return array


sort_pop(candidates)


def select_pop(pop_size):
    """
    Parameters: pop_size(int) - amount of individuals in population
    Returns: best_pop - an array containing the fittest individuals
    """

    for n in range(0, int(pop_size / 2)):
        best_pop.append(candidates[n])
    return best_pop


select_pop(pop_size)

"""
this function can be used to update the fitness in best_pop
def update_fitness():
    for x in best_pop:
        temp = (fitness(x[1]), x[1])
        del x
        best_pop.append(temp)
"""

sort_pop(best_pop)


def tournament():
    """
    Returns: p1, p2 - the fittest two parent grids
    """
    p1 = best_pop[0][1]
    p2 = best_pop[1][1]

    return p1, p2


def crossover():
    """
    Returns: c1, c2 - the two child grids from p1, p2
    """
    grid1, grid2 = tournament()
    crossover_point = random.randint(0, 8)
    p1 = grid1[:crossover_point]
    p11 = grid2[:crossover_point]
    p2 = grid1[crossover_point:]
    p22 = grid2[crossover_point:]

    c1 = np.concatenate((np.array(p1), np.array(p22)))
    c2 = np.concatenate((np.array(p11), np.array(p2)))

    return c1, c2


crossover()


def mutate(board, mutation_rate):
    """
    Parameters: board - the given grid
                mutation_rate - rate at which the population mutates
    Returns: board - returns the mutated board
    """
    pair = []
    for row in range(0, len(board)):
        probability = random.random()
        if probability < 1 - mutation_rate:
            continue
        elif probability >= 1 - mutation_rate:
            for x in range(0, len(board[row])):
                if x in given_indices[row]:
                    continue
                else:
                    pair.append(x)
            sublist = [pair[x:x + 2] for x in range(0, len(pair), 2)]
            for x in sublist:
                if len(x) == 2:
                    board[row][x[0]], board[row][x[1]] = board[row][x[1]], board[row][x[0]]
                else:
                    continue
            pair.clear()
            sublist.clear()
    # returns the mutated board
    return board


def evolve():
    """
    Returns: fitness and generation number
    """
    for gen in range(0, generations):
        population(pop_size)
        sort_pop(candidates)
        select_pop(pop_size)
        c1, c2 = crossover()
        best_pop.pop()
        best_pop.pop()
        best_pop.append((fitness(c1), c1))
        best_pop.append((fitness(c2), c2))
        sort_pop(best_pop)
        for p in range(0, len(best_pop)):
            mutate(best_pop[p][1], mutation_rate)
        sort_pop(best_pop)
        print("\n---------------------------------------------")
        print("\nGENERATION: {}".format(gen))
        print("FITNESS: {}".format(best_pop[0][0]))
        if best_pop[0][0] == 0:
            print("\n---------------------------------------------")
            print("\nSOLUTION FOUND\n")
            print(best_pop[0][1])
            break


evolve()

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
