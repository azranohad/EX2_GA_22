
import copy
import csv
import random


def split_digit_details(str_digit_detail):
    coordinates = (int(str_digit_detail[0]), int(str_digit_detail[1]))
    value = int(str_digit_detail[2])
    return coordinates, value

def get_val_point_to_board(val_point):
    return (val_point*2)-2

def get_coordinates_for_print_board(coordinates):
    return get_val_point_to_board(coordinates[0]), get_val_point_to_board(coordinates[1])

def get_default_board():
    board = []
    for i in range((size_of_matrix * 2) - 1):
        row = []
        for j in range((size_of_matrix * 2) - 1):
            if 0 != i % 2:
                row.append('-')
            elif j % 2 == 1:
                row.append('|')
            else:
                row.append(' ')

        board.append(row)

    return board

def get_symbol_greater(str_greater_sign):
    row_great = get_val_point_to_board(int(str_greater_sign[0]))
    col_great = get_val_point_to_board(int(str_greater_sign[1]))
    row_small = get_val_point_to_board(int(str_greater_sign[2]))
    col_small = get_val_point_to_board(int(str_greater_sign[3]))


    if row_great == row_small:
        coordinates = (row_small, min(col_great, col_small)+1)
        if col_great > col_small:
            return coordinates, '<'
        else:
            return coordinates, '>'

    coordinates = (min(row_small, row_great) + 1, col_small)
    if row_great > row_small:
        return coordinates, '^'
    else:
        return coordinates, 'v'

def set_init_digits_dict():
    for dig in given_digits_details:
        split_digit = split_digit_details(dig)
        coordinates = split_digit[0]
        init_digits_dict[coordinates] = split_digit[1]

def print_board(board):
    board_to_print = get_default_board()

    # for init_digit in init_digits_dict.keys():
    #     coordinates_to_board = get_coordinates_for_board(init_digit)
    #     board[coordinates_to_board[0]][coordinates_to_board[1]] = init_digits_dict.get(init_digit)

    for i in range(size_of_matrix):
        for j in range(size_of_matrix):
            coordinates_to_print_board = get_coordinates_for_print_board((i+1, j+1))
            board_to_print[coordinates_to_print_board[0]][coordinates_to_print_board[1]] = str(board[i][j])

    for greater_symbol in greater_than:
        symbol_and_coordinates_for_map = get_symbol_greater(greater_symbol)
        board_to_print[symbol_and_coordinates_for_map[0][0]][symbol_and_coordinates_for_map[0][1]] = symbol_and_coordinates_for_map[1]

    for row in board_to_print:
        print(row)


def create_first_gen_board():
    board = []


    for r in range(size_of_matrix):
        row = generic_row.copy()
        random.shuffle(row)
        board.append(row)

    return board

def get_row_mismatch(board):
    fitness = 0
    for i in range(size_of_matrix):
        row = set()
        for j in range(size_of_matrix):
            row.add(board[i][j])
        if len(row) != size_of_matrix:
            fitness += 2

    return fitness


def get_col_mismatch(board):
    fitness = 0
    for j in range(size_of_matrix):
        col = set()
        for i in range(size_of_matrix):
            col.add(board[i][j])
        if len(col) != size_of_matrix:
            fitness += 2

    return fitness

def get_init_digits_mismatch(board):
    fitness = 0
    # check init digits
    for digit in init_digits_dict.keys():
        r = digit[0] - 1
        c = digit[1] - 1
        if board[r][c] != init_digits_dict.get(digit):
            fitness += size_of_matrix+1

    return fitness

def get_greater_than_mismatch(board):
    fitness = 0
    for str_greater_sign in greater_than:
        row_great = int(str_greater_sign[0]) - 1
        col_great = int(str_greater_sign[1]) - 1
        row_small = int(str_greater_sign[2]) - 1
        col_small = int(str_greater_sign[3]) - 1

        if board[row_great][col_great] <= board[row_small][col_small]:
            fitness += 1

    return fitness

def get_fitness(board):
    fitness = 0

    fitness += get_init_digits_mismatch(board)
    fitness += get_col_mismatch(board)
    fitness += get_greater_than_mismatch(board)
    fitness += get_row_mismatch(board)

    return fitness

def get_mutation_board(board, num_of_mutation_row):

    mutation_board = board.copy()

    index_random_rows = random.sample(range(0, size_of_matrix), num_of_mutation_row)

    for index_row in index_random_rows:
        row = generic_row.copy()
        random.shuffle(row)
        mutation_board[index_row] = row

    return mutation_board

def get_crossover_board(board_a, board_b, num_row_from_board_b):
    crossover_board = board_a.copy()

    index_random_rows_board_b = random.sample(range(0, size_of_matrix), num_row_from_board_b)

    for index_row in index_random_rows_board_b:
        crossover_board[index_row] = board_b[index_row]

    return crossover_board


def optim_population(population):
    next_population = []
    for element in population:
        optim_board = copy.deepcopy(element[0])
        board = element[0]
        for str_greater_sign in greater_than:
            row_great = int(str_greater_sign[0]) - 1
            col_great = int(str_greater_sign[1]) - 1
            row_small = int(str_greater_sign[2]) - 1
            col_small = int(str_greater_sign[3]) - 1

            if board[row_great][col_great] <= board[row_small][col_small]:
                optim_board[row_great][col_great] = board[row_small][col_small]
                optim_board[row_small][col_small] = board[row_great][col_great]
        board_with_fitness = (optim_board, get_fitness(optim_board))
        next_population.append(board_with_fitness)

    return next_population
    # next_population = []
    # for board in population:
    #     optim_board = board[0].copy()
    #     for j in range(size_of_matrix):
    #         count_array = []
    #         col_array = []
    #         for c in range(size_of_matrix): count_array.append(0)
    #         for i in range(size_of_matrix):
    #             last_val = board[0][i][j]-1
    #             count_array[last_val] = count_array[last_val] + 1
    #             col_array.append(board[0][i][j])
    #
    #
    #         if min(count_array) == 0:
    #             miss_val = count_array.index(0)+1
    #             over_val = count_array.index(max(count_array))+1
    #             optim_board[col_array.index(over_val)][j] = miss_val
    #     next_population.append((optim_board, get_fitness(optim_board)))
    # return next_population


def transfer_generation(population, elite,flag, random_mix = False):
    elite_percent = elite
    next_population = []
    elite_index = 0
    while len(next_population)<elite_percent:
        if population[elite_index] not in next_population:
            next_population.append(population[elite_index])
        elite_index += 1

    len_population = len(population)

    num_of_mutation_row = int(size_of_matrix/2)
    num_row_from_board_b = int(size_of_matrix/2)
    if random_mix:
        num_of_mutation_row = random.randint(1, size_of_matrix-1)
        num_row_from_board_b = random.randint(1, size_of_matrix-1)
    while len(next_population)<len_population:
        i = random.randint(elite_index+1, len_population-1)
        temp_mutation_boards = get_mutation_board(population[i][0], num_of_mutation_row)
        crossover_board = get_crossover_board(population[i % elite_percent][0], temp_mutation_boards, num_row_from_board_b)
        tuple_crossover_board = (crossover_board, get_fitness(crossover_board))
        if tuple_crossover_board not in next_population:
            next_population.append(tuple_crossover_board)
    if flag == 0:
        next_population.sort(key=lambda x: x[1])
        return next_population
    elif flag == 1:
        next_population1 = optim_population(next_population)
        next_population1.sort(key=lambda x: x[1])
        return next_population1
    else:
        darwin = optim_population(next_population)
        darwin.sort(key=lambda x: x[1])
        if darwin[0][1] == 0:
            return darwin
        next_population1 = optim_population(next_population)
        next_population1.sort(key=lambda x: x[1])
        return next_population1

def get_avg_fitness(population):
    sum_fitness = 0
    for board in population:
        sum_fitness += board[1]

    return sum_fitness/len(population)



def generation_loop(init_population, num_of_generation, elite_percent,flag, random_mix = False):
    next_population = init_population.copy()
    avg_fitness_list = []
    best_fitness = []
    for i in range(num_of_generation):
        next_population = transfer_generation(next_population, elite_percent,flag ,random_mix)
        avg_fitness_list.append(get_avg_fitness(next_population))
        best_fitness.append(next_population[0][1])

        if next_population[0][1] == 0:
            return next_population[0][0], avg_fitness_list, best_fitness, next_population

    return next_population[0][0], avg_fitness_list, best_fitness, next_population



def write_to_csv(avg_fitness_list, fitness_best_board, best_fitness, strategy, part):
    row_to_csv = []
    row_to_csv.append("size of matrix:" + str(size_of_matrix))
    row_to_csv.append("difficulty:" + difficulty)
    row_to_csv.append(strategy)
    writer.writerow(row_to_csv)

    row_to_csv = []
    row_to_csv.append(len(avg_fitness_list))
    row_to_csv.append(fitness_best_board)
    row_to_csv.append(part)
    writer.writerow(row_to_csv)
    writer.writerow(avg_fitness_list)
    writer.writerow(best_fitness)

def start(flag):
    #print('size of matrix: ' + str(size_of_matrix) + ", difficulty: " + difficulty)
    population = []

    for i in range(100):
        random_board = create_first_gen_board()
        population.append((random_board, get_fitness(random_board)))
    population.sort(key=lambda x: x[1])

    next_population = population.copy()

    best_board, avg_fitness_list, best_fitness, next_population = generation_loop(next_population, 10000, 30, flag)
    fitness_best_board = get_fitness(best_board)
    print("number of iterations:" + str(len(avg_fitness_list)) + " left to fitness:" + str(fitness_best_board) + ' part 1')
    # print(avg_fitness_list)
    # print(best_fitness)
    #write_to_csv(avg_fitness_list, fitness_best_board, best_fitness, "genetic", 'part 1')
    if fitness_best_board == 0:
        print_board(best_board)
        return best_board
    else:
        print("No answer part 1")

    best_board, avg_fitness_list, best_fitness, next_population = generation_loop(population.copy(), 10000, 25, flag, True)
    fitness_best_board = get_fitness(best_board)
    print("number of iterations:" + str(len(avg_fitness_list)) + " left to fitness:" + str(fitness_best_board) + ' part 2')
    # print(avg_fitness_list)
    # print(best_fitness)
    #write_to_csv(avg_fitness_list, fitness_best_board, best_fitness, "genetic", 'part 2')
    if fitness_best_board == 0:
        print_board(best_board)
        return best_board
    else:
        print("No answer part 2")

    best_board, avg_fitness_list, best_fitness, next_population = generation_loop(population.copy(), 10000, 45, flag, True)
    fitness_best_board = get_fitness(best_board)
    print("number of iterations:" + str(len(avg_fitness_list)) + " left to fitness:" + str(fitness_best_board) + ' part 3'
                                                                                                                 '')
    # print(avg_fitness_list)
    # print(best_fitness)
    #write_to_csv(avg_fitness_list, fitness_best_board, best_fitness, "genetic", 'part 3')
    if fitness_best_board == 0:
        print_board(best_board)
        return best_board
    else:
        print("No answer part 3")


file = open('result.csv', 'w', newline='')
writer = csv.writer(file)

#####################load from file###############################
f = open('Unnecessary.txt')


size_of_matrix = int(f.readline().rstrip('\n'))
#difficulty = "easy"
given_digits = f.readline().rstrip('\n')
given_digits_details = []
for i in range(int(given_digits)):
    given_digits_details.append(f.readline().rstrip('\n'))
greater_than = []
number_of_greater_than = f.readline().rstrip('\n')
for j in range(int(number_of_greater_than)):
    greater_than.append(f.readline().rstrip('\n'))

init_digits_dict = {}
set_init_digits_dict()
generic_row = []    #[1,2,3,4,5....]
for i in range(int(size_of_matrix)):
    generic_row.append(i + 1)
print('size_of_matrix:' + str(size_of_matrix) +' type: genetic')
start(int(0))
print('size_of_matrix:' + str(size_of_matrix) +' type: lemark')
start(int(1))
print('size_of_matrix:' + str(size_of_matrix) +' type: darwin')
start(int(2))

#
# #####################5 easy##################################
# size_of_matrix = 5
# difficulty = "easy"
# given_digits_details = ['143']
# given_digits = len(given_digits_details)
# greater_than = ['1413', '1415', '2111', '2223', '2425', '3343', '3545', '4151', '5352']
# number_of_greater_than = len(greater_than)
#
# init_digits_dict = {}
# set_init_digits_dict()
# generic_row = []    #[1,2,3,4,5....]
# for i in range(size_of_matrix):
#     generic_row.append(i + 1)
# print('size_of_matrix:' + str(size_of_matrix) +', dificault: easy, genetic/darwin/lemark')
# start()
#
# #####################5 tricky##################################
# size_of_matrix = 5
# difficulty = "tricky"
#
# given_digits_details = ['122', '552']
# given_digits = len(given_digits_details)
# greater_than = ['1211', '1514', '2535', '3231', '4151', '4342', '5545', '5152', '5453']
# number_of_greater_than = len(greater_than)
#
# init_digits_dict = {}
# set_init_digits_dict()
# generic_row = []    #[1,2,3,4,5....]
# for i in range(size_of_matrix):
#     generic_row.append(i + 1)
#
# start()
#
# #####################6 easy##################################
# size_of_matrix = 6
# difficulty = "easy"
#
# given_digits_details = ['321', '411', '554', '614', '622', '625']
# given_digits = len(given_digits_details)
# greater_than = ['1112', '3424', '3525', '3334', '3435', '4252', '5545', '5554', '5464']
# number_of_greater_than = len(greater_than)
# init_digits_dict = {}
# set_init_digits_dict()
# generic_row = []    #[1,2,3,4,5....]
# for i in range(size_of_matrix):
#     generic_row.append(i + 1)
#
# start()
#
# #####################6 tricky##################################
# size_of_matrix = 6
# difficulty = "tricky"
#
# given_digits_details = ['155', '331', '514']
# given_digits = len(given_digits_details)
# greater_than = ['2111', '2212', '2425', '3423', '2636', '3141', '3545', '4636', '4142', '4555', '5646', '5453', '6362']
# number_of_greater_than = len(greater_than)
# init_digits_dict = {}
# set_init_digits_dict()
# generic_row = []    #[1,2,3,4,5....]
# for i in range(size_of_matrix):
#     generic_row.append(i + 1)
#
# start()
#
# #####################7 easy##################################
# size_of_matrix = 7
# difficulty = "easy"
#
# given_digits_details = ['116', '152']
# given_digits = len(given_digits_details)
# greater_than = ['1415', '1716', '1626', '2221', '2423', '3424', '3233', '3343', '3536', '3747', '5343', '4546','5455' \
#                 , '6454', '6555', '5666', '6263', '6364', '6676', '6777', '7271', '7374', '7576']
# number_of_greater_than = len(greater_than)
# init_digits_dict = {}
# set_init_digits_dict()
# generic_row = []    #[1,2,3,4,5....]
# for i in range(size_of_matrix):
#     generic_row.append(i + 1)
#
# start()
#
# #####################7 tricky##################################
# size_of_matrix = 7
# difficulty = "tricky"
#
# given_digits_details = ['175', '263', '373', '413']
# given_digits = len(given_digits_details)
# greater_than = ['1121', '1413', '1516', '2322', '3323', '3536', '4636', '5141', '4252', '4342', '4546', '5747','5251' \
#                 , '5253', '5363', '5565', '5655', '6757', '6171', '6162', '7767', '7475', '7576']
# number_of_greater_than = len(greater_than)
# init_digits_dict = {}
# set_init_digits_dict()
# generic_row = []    #[1,2,3,4,5....]
# for i in range(size_of_matrix):
#     generic_row.append(i + 1)
#
# start()

file.close()

while(1):
    nothing = 0