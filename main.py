# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def split_digit_details(str_digit_detail):
    coordinates = (int(str_digit_detail[0]), int(str_digit_detail[1]))
    value = int(str_digit_detail[2])
    return coordinates, value

def get_val_point_to_board(val_point):
    return (val_point*2)-2
def get_coordinates_for_board(coordinates):
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

def set_init_board():
    board = get_default_board()

    for init_digit in init_digits_dict.keys():
        coordinates_to_board = get_coordinates_for_board(init_digit)
        board[coordinates_to_board[0]][coordinates_to_board[1]] = init_digits_dict.get(init_digit)

    for greater_symbol in greater_than:
        symbol_and_coordinates_for_map = get_symbol_greater(greater_symbol)
        board[symbol_and_coordinates_for_map[0][0]][symbol_and_coordinates_for_map[0][1]] = symbol_and_coordinates_for_map[1]

    print_board(board)


def print_board(board):
    for row in board:
        print(row)


size_of_matrix = 5
given_digits = 2
given_digits_details = ['124', '332']
greater_than = ['1112', '1424', '2223', '3444', '4535', '4454', '5545', '5251']
number_of_greater_than = len(greater_than)
init_digits_dict = {}
set_init_digits_dict()


set_init_board()
x = 3

