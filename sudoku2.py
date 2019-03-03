from random import choice
import numpy as np

def is_eligible(sudoku, row_index, col_index, num):
    if num in sudoku[row_index,:] or num in sudoku[:,col_index]:
        return False
    if within_box(sudoku, row_index, col_index, num):
        return False
    return True

def within_box(sudoku, row_index, col_index, num):
    switcher = {0:2,
                1:1,
                2:0}

    last_row_of_box = row_index + switcher.get(row_index % 3)
    last_col_of_box = col_index + switcher.get(col_index % 3)
    row_index -= row_index % 3
    col_index -= col_index % 3

    #actual checking
    if num in sudoku[row_index:last_row_of_box, col_index:last_col_of_box]:
        return True

    return False

#========================================================================================================
def returnEmptyIndex(sudoku):
    for (row, col), value in np.ndenumerate(sudoku):
        if value == 0:
            return row, col
    return -1, -1

#========================================================================================================

def randomised_sudokuSolver(sudoku):
    row, col = returnEmptyIndex(sudoku)
    if row != -1:
        numbers = [i for i in range(1,10)]
        while len(numbers) > 0:
            num = numbers.pop(numbers.index(choice(numbers)))
            if is_eligible(sudoku, row, col, num):
                sudoku[row, col] = num
                _random = randomised_sudokuSolver(sudoku)
                if returnEmptyIndex(sudoku) == (-1, -1):
                    #SUDOKU COMPLETE
                    return True
                sudoku[row, col] = 0
    else:
        return False

def sudokuSolver(sudoku):
    row, col = returnEmptyIndex(sudoku)
    if row != -1:
        for num in range(1,10):
            if is_eligible(sudoku, row, col, num):
                sudoku[row, col] = num
                _random = sudokuSolver(sudoku)
                if returnEmptyIndex(sudoku) == (-1, -1):
                    #SUDOKU COMPLETE
                    return True
                sudoku[row, col] = 0
    else:
        return False

# #DRIVER
# sudoku = np.array([ [7, 0, 0, 5, 0, 0, 0, 6, 8],
#                     [0, 6, 2, 0, 0, 4, 0, 3, 0],
#                     [3, 0, 0, 0, 6, 0, 2, 0, 0],
#                     [0, 5, 0, 0, 0, 2, 7, 0, 9],
#                     [1, 0, 9, 6, 0, 0, 0, 0, 0],
#                     [0, 0, 0, 0, 1, 0, 5, 0, 6],
#                     [0, 0, 1, 0, 4, 0, 6, 7, 0],
#                     [2, 8, 0, 1, 0, 7, 0, 0, 0],
#                     [0, 0, 7, 0, 3, 0, 8, 0, 1]])
# randomised_sudokuSolver(sudoku)
# print(sudoku)