# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import statistics


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
            fitness += 1

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

def transfer_generation(population, elite, random_mix = False):
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


    next_population.sort(key=lambda x: x[1])
    return next_population

def get_avg_fitness(population):
    sum_fitness = 0
    for board in population:
        sum_fitness += board[1]

    return sum_fitness/len(population)



def generation_loop(init_population, num_of_generation, elite_percent, random_mix = False):
    next_population = init_population.copy()
    avg_fitness_list = []
    for i in range(num_of_generation):
        next_population = transfer_generation(next_population, elite_percent, random_mix)
        avg_fitness_list.append(get_avg_fitness(next_population))

        if next_population[0][1] == 0:
            return next_population[0][0], avg_fitness_list, next_population

    return next_population[0][0], avg_fitness_list, next_population




def start():
    population = []
    for i in range(100):
        random_board = create_first_gen_board()
        population.append((random_board, get_fitness(random_board)))
    population.sort(key=lambda x: x[1])

    next_population = population.copy()

    best_board, avg_fitness_list, next_population = generation_loop(next_population, 10000, 50)
    fitness_best_board = get_fitness(best_board)
    if fitness_best_board == 0:
        print_board(best_board)
        print(len(avg_fitness_list), fitness_best_board)
        return best_board


    best_board, avg_fitness_list, next_population = generation_loop(population.copy(), 10000, 30, True)
    fitness_best_board = get_fitness(best_board)
    print_board(best_board)
    print(len(avg_fitness_list), fitness_best_board)
    if fitness_best_board == 0:
        return best_board

    best_board, avg_fitness_list, next_population = generation_loop(population.copy(), 10000, 20, True)
    fitness_best_board = get_fitness(best_board)
    print_board(best_board)
    print(len(avg_fitness_list), fitness_best_board)
    if fitness_best_board == 0:
        return best_board

    fitness_best_board = get_fitness(best_board)
    print(len(avg_fitness_list), fitness_best_board)
    return best_board










size_of_matrix = 7
given_digits = 2
given_digits_details = ['124', '332']
greater_than = ['1112', '1424', '2223', '3444', '4535', '4454', '5545', '5251']
number_of_greater_than = len(greater_than)
init_digits_dict = {}
set_init_digits_dict()
generic_row = []    #[1,2,3,4,5....]
for i in range(size_of_matrix):
    generic_row.append(i + 1)


start()

# get_fitness(population[0])
# set_board_print(population[0])

x = 3

