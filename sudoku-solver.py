#!/usr/bin/env python3
# coding=utf-8
# Version 0.1

##############################
# IMPORTS                    #
##############################

from math import ceil, floor

##############################
# FUNCTIONS                  #
##############################


def ask_total_rows():
    total_rows = 0
    try:
        total_rows = int(input("Total rows: "))
    except ValueError:
        print("The input is not an integer.")
        ask_total_rows()
    return total_rows


def ask_total_columns():
    total_columns = 0
    try:
        total_columns = int(input("Total columns: "))
    except ValueError:
        print("The input is not an integer.")
        ask_total_columns()
    return total_columns


def ask_squares_number():
    squares_number = 0
    try:
        squares_number = int(input("Squares's number: "))
    except ValueError:
        print("The input is not an integer.")
        ask_squares_number()
    return squares_number


def ask_square_rows_number():
    square_rows_number = 0
    try:
        square_rows_number = int(input("Square's rows number: "))
    except ValueError:
        print("The input is not an integer.")
        ask_square_rows_number()
    return square_rows_number


def ask_square_columns_number():
    square_columns_number = 0
    try:
        square_columns_number = int(input("Square's columns number: "))
    except ValueError:
        print("The input is not an integer.")
        ask_square_columns_number()
    return square_columns_number


def ask_empty_sudoku_grid(total_rows, total_columns):
    grid_values = []
    for row in range(total_rows):
        line = []
        for col in range(total_columns):
            value = 0
            try:
                value = int(input("Value in row " + str(row + 1) + ", column " + str(col + 1) + " (0 for empty): "))
            except ValueError:
                print("The input is not an integer.")
            line.append(value)
        grid_values.append(line)
    return grid_values


def draw_separate_line(total_columns, square_columns):
    separate_line = "+-"
    squares_number_by_row = ceil((int(total_columns) / int(square_columns)))
    for square in range(squares_number_by_row):
        for col in range(square_columns):
            separate_line += "--"
        separate_line += "+-"
    separate_line = separate_line[:-1] + "\n"
    return separate_line


def draw_sudoku_grid(grid_values, first_row_to_draw, last_row_to_draw, first_column_to_draw, last_column_to_draw, squares_number, square_rows_number, square_columns_number): # noqa
    grid_drawing = ""
    for row in range(first_row_to_draw, last_row_to_draw):
        if ((row + 1) % square_rows_number) == 1:
            grid_drawing += draw_separate_line(squares_number, square_columns_number)
        for col in range(first_column_to_draw, last_column_to_draw):
            value = grid_values[row][col]
            if ((col + 1) % square_columns_number) == 1:
                grid_drawing += "| "
            if value == 0:
                grid_drawing += ". "
            else:
                grid_drawing += str(value) + " "
        grid_drawing += "| \n"

    grid_drawing += draw_separate_line(squares_number, square_columns_number)
    print(grid_drawing)


def resolve_sudoku_grid(verbose, grid_values, square_rows_number, square_columns_number):
    # In the early version, we'll handle the square grid only.
    # It's why, the value range = the columns range or the rows range
    # The values range are the value we have to put in the grid (initially 1 to 9)
    values_range = range(total_columns)
    total_number_of_empty_boxes = 0
    for row in range(total_rows):
        for column in range(total_columns):
            if grid_values[row][column] == 0:
                total_number_of_empty_boxes += 1

    print("Total number of empty boxes = " + str(total_number_of_empty_boxes) + "\n")
    while total_number_of_empty_boxes > 0:
        # For each empty boxes in the grid
        for row in range(total_rows):
            for column in range(total_columns):
                # We retrieve all the possible values we can put on this box,
                # just by checking the line, the column and the square.
                possible_values_in_current_box = []
                if verbose:
                    print("-------------------------------------------------------------------------------------------")
                    print("Let's check the box on line " + str(row + 1) + " column " + str(column + 1) + ".")
                # Value == 0 means empty box.
                if grid_values[row][column] == 0:
                    if verbose:
                        print("The box is empty, we can search the value.\n")
                    # Values range = {1, 2, 3, 4, 5, 6, 7, 8, 9} in classic sudoku 9x9
                    for value_to_check in values_range:
                        # As python range starts from 0 and sudoku starts from 1, I add 1 to the python range's value.
                        value_to_check = value_to_check + 1
                        if verbose:
                            print("Is it possible to write the value " + str(value_to_check) + " in this box ?")
                        # Horizontal check
                        if verbose:
                            print("\tHorizontal check:")
                            print("\t\tThe others numbers in the same line are: " + str(grid_values[row]))
                        if value_to_check not in grid_values[row]:
                            if verbose:
                                print("\t\tYes, it is possible, so we are now doing the vertical check.")
                        else:
                            if verbose:
                                print("\t\tNo, " + str(value_to_check) + " can not be on this box because it already exists on this line.\n") # noqa
                            continue

                        # Vertical check
                        if verbose:
                            print("\tVertical check:")
                        values_on_the_same_column = []
                        for horizontal_index in range(len(grid_values)):
                            values_on_the_same_column.append(grid_values[horizontal_index][column])
                        if verbose:
                            print("\t\tThe others numbers in the same column are: " + str(values_on_the_same_column))

                        if value_to_check not in values_on_the_same_column:
                            if verbose:
                                print("\t\tYes, it is possible, so we are now doing the square check.")
                        else:
                            if verbose:
                                print("\t\tNo, " + str(value_to_check) + " can not be on this box because it already exists on this column.\n") # noqa
                            continue

                        # Square check
                        first_square_row = floor(row / square_rows_number) * square_rows_number
                        last_square_row = floor((row + square_rows_number) / square_rows_number) * square_rows_number
                        first_square_column = floor(column / square_columns_number) * square_columns_number
                        last_square_column = floor((column + square_columns_number) / square_columns_number) * square_columns_number # noqa
                        if verbose:
                            print("\tSquare check:")
                        values_on_the_current_square = []
                        for square_row in range(first_square_row, last_square_row):
                            line = []
                            for square_column in range(first_square_column, last_square_column):
                                line.append(grid_values[square_row][square_column])
                            values_on_the_current_square.append(line)
                        if verbose:
                            print("\t\tThe others numbers in the same square are:" + str(values_on_the_current_square))
                        if value_to_check not in values_on_the_current_square:
                            if verbose:
                                print("\t\tYes, it is possible, so we are now adding the value " + str(value_to_check) + " to the possible list of values of this box.") # noqa
                            possible_values_in_current_box.append(value_to_check)
                        else:
                            if verbose:
                                print("\t\tNo, " + str(value_to_check) + " can not be on this box because it already exists on this square.\n") # noqa
                        if verbose:
                            draw_sudoku_grid(grid_values, first_square_row, last_square_row, first_square_column, last_square_column, 1, square_rows_number, square_columns_number) # noqa
                    if verbose:
                        print("Box " + str(row + 1) + ":" + str(column + 1) + " = " + str(possible_values_in_current_box))
                if len(possible_values_in_current_box) == 1:
                    grid_values[row][column] = possible_values_in_current_box[0]
                    total_number_of_empty_boxes -= 1


##############################
# MAIN                       #
##############################

# squares_number = ask_squares_number()
# square_rows_number = ask_square_rows_number()
# square_columns_number = ask_square_columns_number()
# total_rows = ask_total_rows()
# total_columns = ask_total_columns()
# grid_values = ask_empty_sudoku_grid(total_rows, total_columns)

squares_number = 4
square_rows_number = 2
square_columns_number = 2
total_rows = 4
total_columns = 4
grid_values = [[0, 0, 0, 1], [0, 1, 3, 0], [0, 2, 0, 0], [4, 0, 0, 0]]

print("Here the grid you drew, is that right ?")
draw_sudoku_grid(grid_values, 0, total_rows, 0, total_columns, squares_number, square_rows_number, square_columns_number) # noqa

resolve_sudoku_grid(True, grid_values, square_rows_number, square_columns_number)

print("Here the solution:")
draw_sudoku_grid(grid_values, 0, total_rows, 0, total_columns, squares_number, square_rows_number, square_columns_number) # noqa
