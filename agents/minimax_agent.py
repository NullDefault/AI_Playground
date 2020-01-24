from agents.agent import Agent


def flip_team(team):
    if team == 'x':
        return 'o'
    else:
        return 'x'


def evaluate_board(game_board, max):

    cells = game_board.cells

    if max == 'x':
        max = 1
        mini = 0
    elif max == 'o':
        max = 0
        mini = 1

    # Checking for Rows for X or O victory.
    for row in range(0, 3):

        if cells[row, 0].state == cells[row, 1].state and cells[row, 1].state == cells[row, 2].state:

            if cells[row, 0].state == max:
                return 10
            elif cells[row, 0].state == mini:
                return -10

                # Checking for Columns for X or O victory.
    for col in range(0, 3):

        if cells[0, col].state == cells[1, col].state and cells[1, col].state == cells[2, col].state:

            if cells[0, col].state == max:
                return 10
            elif cells[0, col].state == mini:
                return -10

                # Checking for Diagonals for X or O victory.
    if cells[0, 0].state == cells[1, 1].state and cells[1, 1].state == cells[2, 2].state:

        if cells[0, 0].state == max:
            return 10
        elif cells[0, 0].state == mini:
            return -10

    if cells[0, 2].state == cells[1, 1].state and cells[1, 1].state == cells[2, 0].state:

        if cells[0, 2].state == max:
            return 10
        elif cells[0, 2].state == mini:
            return -10

            # Else if none of them have won then return 0
    return 0


class MinMaxAgent(Agent):

    def __init__(self, name, team):
        self.team = team
        Agent.__init__(self, name)

    def take_turn(self, game_board):
        turn_choice = self.minimax(game_board, 0, self.team)
        return turn_choice

    def minimax(self, board, depth, maximizing_player):
        terminal_state = evaluate_board(board, maximizing_player)
        if terminal_state:
            return terminal_state

        if maximizing_player == self.team:      # TODO: save the best move
            best_val = -100000
            best_move = None
            for move in board.possible_moves:
                if board.cells[move].state is -1:
                    new_board = board.make_move(move, self.team)
                    value = self.minimax(new_board, depth + 1, self.team)
                    if type(value) is tuple:
                        return value
                    elif value >= best_val:
                        best_val = value
                        best_move = move
            return best_move
        else:
            best_val = 100000
            best_move = None
            for move in board.possible_moves:
                if board.cells[move].state is -1:
                    new_board = board.make_move(move, self.team)
                    value = self.minimax(new_board, depth + 1, self.team)
                    if type(value) is tuple:
                        return value
                    elif value < best_val:
                        best_val = value
                        best_move = move
            return best_move
