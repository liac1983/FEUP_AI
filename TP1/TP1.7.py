from collections import deque
from copy import deepcopy
import heapq

# definition of the problem
class NPuzzleState:

    def __init__(self, board, move_history=[]):
        self.board = deepcopy(board)
        (self.blank_row, self.blank_col) = self.find_blank()
        self.move_history = [] + move_history + [self.board]

    def children(self):
        functions = [self.up, self.down, self.left, self.right]
        children = []
        for func in functions:
            child = func()
            if child:
                children.append(child)
        return children

    def find_blank(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return (row, col)

    def move(func):
        def wrapper(self):
            state = NPuzzleState(self.board, self.move_history)
            value = func(state)
            if value:
                return state
            else:
                return None
        return wrapper

    @move
    def up(self):
        if self.blank_row == 0:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row - 1][self.blank_col]
            self.board[self.blank_row - 1][self.blank_col] = 0
            self.blank_row -= 1
            return True

    @move
    def down(self):
        if self.blank_row == len(self.board) - 1:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row + 1][self.blank_col]
            self.board[self.blank_row + 1][self.blank_col] = 0
            self.blank_row += 1
            return True

    @move
    def left(self):
        if self.blank_col == 0:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row][self.blank_col - 1]
            self.board[self.blank_row][self.blank_col - 1] = 0
            self.blank_col -= 1
            return True

    @move
    def right(self):
        if self.blank_col == len(self.board[0]) - 1:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row][self.blank_col + 1]
            self.board[self.blank_row][self.blank_col + 1] = 0
            self.blank_col += 1
            return True

    def is_complete(self):
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __hash__(self):
        return hash(str([item for sublist in self.board for item in sublist]))

    def __eq__(self, other):
        return [item for sublist in self.board for item in sublist] == [item for sublist in other.board for item in sublist]

def print_sequence(sequence):
    print("Steps:", len(sequence) - 1)
    for state in sequence:
        for row in state:
            print(row)
        print()

def problems():
    return (
        NPuzzleState([[1, 2, 3], [5, 0, 6], [4, 7, 8]]),
        NPuzzleState([[1, 3, 6], [5, 2, 0], [4, 7, 8]]),
        NPuzzleState([[1, 6, 2], [5, 7, 3], [0, 4, 8]]),
        NPuzzleState([[5, 1, 3, 4], [2, 0, 7, 8], [10, 6, 11, 12], [9, 13, 14, 15]]),
    )

def bfs(problem):
    queue = deque([problem])
    visited = set()
    while queue:
        state = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        if state.is_complete():
            return state.move_history
        for child in state.children():
            queue.append(child)
    return None

print_sequence(bfs(problems()[2]))
