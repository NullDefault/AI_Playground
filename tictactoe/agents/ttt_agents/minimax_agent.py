'''
Agent that uses the minimax algorithm to make their moves
'''

from tictactoe.agents.ttt_agents.agent import Agent
from random import randint

'''
col:     0  1  2  
row:  0 [0][1][2]
      1 [3][4][5]
      2 [6][7][8]
'''


def are_there_moves_left(board_array):
    for i in range(3):
        for j in range(3):
            if board_array[(i, j)] == -1:
                return True
    else:
        return False


def is_it_first_turn(board_array):
    for i in range(3):
        for j in range(3):
            if board_array[(i, j)] != -1:
                return False
    else:
        return True


class Move:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class MinMaxAgent(Agent):

    def __init__(self, name, team):
        self.team = team
        if team == 'x':
            self.opponent = 'o'
        else:
            self.opponent = 'x'
        Agent.__init__(self, name)

    def take_turn(self, game_board):
        board = game_board.cells
        # If it's the first turn, we randomly choose one of the cells
        if is_it_first_turn(board):
            x = randint(0, 2)
            y = randint(0, 2)
            return x, y
        # Otherwise we use minmax
        turn_choice = self.find_best_move(board)
        return turn_choice

    def find_best_move(self, board):

        if self.team == 'x':
            team = 1
        elif self.team == 'o':
            team = 0

        best_value = -1000
        best_move = Move(-1, -1)

        for i in range(3):
            for j in range(3):
                if board[i][j] == -1:

                    board[i][j] = team

                    move_value = self.minimax(board, 0, False)

                    board[i][j] = -1

                    if move_value > best_value:
                        best_move.row = i
                        best_move.column = j
                        best_value = move_value

        return best_move.row, best_move.column

    def minimax(self, board, depth, is_maximizing_player):
        if self.team == 'x':
            team = 1
            opponent = 0
        elif self.team == 'o':
            team = 0
            opponent = 1

        board_score = self.evaluate_board(board)

        if board_score is not 0:
            return board_score - depth

        if not are_there_moves_left(board):
            return 0

        if is_maximizing_player:
            best_value = -1000

            for i in range(3):
                for j in range(3):
                    if board[i][j] == -1:
                        board[i][j] = team

                        best_value = max(best_value, self.minimax(board, depth+1, not is_maximizing_player))

                        board[i][j] = -1

            return best_value

        else:
            best_value = 1000

            for i in range(3):
                for j in range(3):
                    if board[i][j] == -1:
                        board[i][j] = opponent

                        best_value = min(best_value, self.minimax(board, depth+1, not is_maximizing_player))

                        board[i][j] = -1

            return best_value

    def evaluate_board(self, board_array):

        if self.team == 'x':
            team = 1
            opponent = 0
        elif self.team == 'o':
            team = 0
            opponent = 1

        for row in range(3):
            if board_array[row][0] == board_array[row][1] == board_array[row][2]:
                if board_array[row][0] == team:
                    return +10
                elif board_array[row][0] == opponent:
                    return -10

        for column in range(3):
            if board_array[0][column] == board_array[1][column] == board_array[2][column]:
                if board_array[0][column] == team:
                    return +10
                elif board_array[0][column] == opponent:
                    return -10

        if board_array[0][0] == board_array[1][1] == board_array[2][2]:
            if board_array[0][0] == team:
                return +10
            elif board_array[0][0] == opponent:
                return -10

        if board_array[0][2] == board_array[1][1] == board_array[2][0]:
            if board_array[0][2] == team:
                return +10
            elif board_array[0][2] == opponent:
                return -10

        return 0