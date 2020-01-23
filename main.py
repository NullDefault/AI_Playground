import pygame
from agents.human_player import HumanPlayer
from fysom import Fysom


class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = self.init_cells(rows, columns)

    def init_cells(self, rows, columns):
        cells = {}

        for r in range(rows):
            for c in range(columns):
                cells[(r, c)] = BoardCell((r, c))

        return cells

    def check_win_con(self, last_move):
        x = last_move[0]
        y = last_move[1]

        # check if previous move caused a win on vertical line
        if self.cells[(0, y)].state == self.cells[(1, y)].state == self.cells[(2, y)].state:
            return True

        # check if previous move caused a win on horizontal line
        if self.cells[(x, 0)].state == self.cells[(x, 1)].state == self.cells[(x, 2)].state:
            return True

        # check if previous move was on the main diagonal and caused a win
        if x == y and self.cells[(0, 0)].state == self.cells[(1, 1)].state == self.cells[(2, 2)].state:
            return True

        # check if previous move was on the secondary diagonal and caused a win
        if x + y == 2 and self.cells[(0, 2)].state == self.cells[(1, 1)].state == self.cells[(2, 0)].state:
            return True

        return False


empty_sprite = pygame.image.load("empty_sprite.png")
x_sprite = pygame.image.load("x_sprite.png")
o_sprite = pygame.image.load("o_sprite.png")


class BoardCell:
    def __init__(self, loc):
        self.state = -1  # -1 is empty, 0 is O, 1 is X
        self.loc = loc   # The x, y coordinates of the cell on the game board
        self.image = self.update_sprite()

    def set_x(self):
        self.state = 1
        self.image = self.update_sprite()

    def set_o(self):
        self.state = 0
        self.image = self.update_sprite()

    def clear(self):
        self.state = -1
        self.image = self.update_sprite()

    def update_sprite(self):
        if self.state == -1:
            return empty_sprite
        elif self.state == 0:
            return o_sprite
        elif self.state == 1:
            return x_sprite


def main():
    game_surface = pygame.display.set_mode((700, 600))

    row_num = 3
    column_num = 3
    game_board = Board(row_num, column_num)

    game_state = Fysom({
        'initial': 'x_turn',
        'events': [
            {'name': 'x_turn_taken', 'src': 'x_turn', 'dst': 'o_turn'},
            {'name': 'o_turn_taken', 'src': 'o_turn', 'dst': 'x_turn'},
            {'name': 'x_wins', 'src': 'x_turn', 'dst': 'game_over'},
            {'name': 'o_wins', 'src': 'o_turn', 'dst': 'game_over'}
        ]
    })

    players = (HumanPlayer(0), HumanPlayer(1))
    winner = None

    def render():
        for r in range(row_num):
            for c in range(column_num):
                cell = game_board.cells[(r, c)]
                game_surface.blit(cell.image, (cell.loc[0]*200, cell.loc[1]*200))

    while True:
        render()
        pygame.display.flip()

        if game_state.current == 'x_turn':
            move = players[0].take_turn(game_board)
            game_board.cells[move].set_x()
            win = game_board.check_win_con(move)
            if win:
                game_state.trigger('x_wins')
                winner = 'X'
            else:
                game_state.trigger('x_turn_taken')

        elif game_state.current == 'o_turn':
            move = players[1].take_turn(game_board)
            game_board.cells[move].set_o()
            win = game_board.check_win_con(move)
            if win:
                game_state.trigger('o_wins')
                winner = 'O'
            else:
                game_state.trigger('o_turn_taken')

        elif game_state.current == 'game_over':
            print(winner)


if __name__ == "__main__":
    main()
