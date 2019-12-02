import cv2
import numpy as np

# This is a board class it holds an array and many fucntions to solve the sudoku puzzle
# Always a 9x9 puzzle
class board:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def get_row(self, row_num):
        return self.puzzle[row_num]

    def get_col(self, col_num):
        return [row[col_num] for row in self.puzzle]

    def get_box(self, row_num, col_num):
        box = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]
        base_row = 3 * int(row_num / 3)
        base_col = 3 * int(col_num / 3)
        for i in range(0, 3):
            for j in range(0, 3):
                box[i][j] = self.puzzle[base_row + i][base_col + j]

        return box

    def find_next_empty(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.puzzle[i][j] == 0:
                    return i, j
        return -1, -1

    def valid_option(self, row_num, col_num, number):
        if self.puzzle[row_num][col_num] != 0:
            return False
        if number in self.get_row(row_num):
            return False
        if number in self.get_col(col_num):
            return False
        box = self.get_box(row_num, col_num)
        for row in box:
            if number in row:
                return False
        return True

    # Using backtrack algorithm
    def solve_recursive(self):
        # Find our next spot to put a number
        x, y = self.find_next_empty()
        # Base case we have finished the puzzle
        if x == -1:
            return True, self.puzzle
        if y == -1:
            return True, self.puzzle
        # For each number 1-9 if it is valid
        for i in range(1, 10):
#            print("try: ", i)
#            print(self.puzzle)
            # if that number works in the current puzzle
            if self.valid_option(x, y, i):
                # Add that number to a new board and solve it
                new_board = self.puzzle.copy()
                new_board[x][y] = i
                print(new_board)
                temp = board(new_board)
                solved, puzzle = temp.solve_recursive()
                # if that solves the puzzle return
                if solved:
                    return solved, puzzle
                else:
#                    print(i, ": failed")
#                    print(puzzle)
                    continue
            # if not continue
        # If there are no options in this spot given the current board
        # return false
        return False, None

a = np.array([[0, 0, 0,   0, 0, 0,   0, 0, 0],
              [0, 0, 0,   0, 0, 0,   0, 0, 0],
              [0, 0, 0,   0, 0, 0,   0, 0, 0],

              [0, 0, 0,   0, 0, 0,   0, 0, 0],
              [0, 0, 0,   0, 0, 0,   0, 0, 0],
              [0, 0, 0,   0, 0, 0,   0, 0, 0],

              [0, 0, 0,   0, 0, 0,   0, 0, 0],
              [0, 0, 0,   0, 0, 0,   0, 0, 0],
              [0, 0, 0,   0, 0, 0,   0, 0, 0]])

p = np.array([[9, 0, 8,   0, 0, 0,   7, 0, 0],
              [1, 0, 0,   0, 0, 9,   0, 0, 4],
              [0, 0, 0,   5, 7, 8,   6, 9, 0],

              [0, 0, 0,   0, 0, 4,   0, 2, 0],
              [3, 4, 0,   7, 0, 0,   0, 0, 0],
              [0, 0, 6,   0, 0, 0,   0, 0, 0],

              [6, 2, 9,   3, 0, 5,   1, 0, 8],
              [0, 5, 0,   0, 6, 0,   0, 0, 0],
              [0, 0, 3,   2, 0, 0,   9, 0, 0]])

b = board(p)

print(b.get_row(5))
print(b.get_col(8))
print(b.get_box(5, 8))
print(b.find_next_empty())
print(b.valid_option(0, 0, 5))
print(b.valid_option(0, 4, 4))
print(b.valid_option(2, 4, 6))
print(b.valid_option(6, 5, 1))
print(b.valid_option(5, 7, 5))
print(b.puzzle)
solve, puzzle = b.solve_recursive()
print(solve)
print(b.puzzle)
print(puzzle)
