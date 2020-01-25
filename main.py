import pygame
import copy
from agents.human_player import HumanPlayer
from agents.random_agent import RandomAgent
from agents.minimax_agent import MinMaxAgent, evaluate_board
from fysom import Fysom


class Board:
    def __init__(self, old_cells=None):
        if old_cells is None:
            self.cells = self.init_cells(3, 3)
            self.board_state = Fysom({      # Game flow is controlled using a finite state machine
                'initial': 'x_turn',
                'events': [
                    {'name': 'x_turn_taken', 'src': 'x_turn', 'dst': 'o_turn'},
                    {'name': 'o_turn_taken', 'src': 'o_turn', 'dst': 'x_turn'},
                    {'name': 'x_wins', 'src': 'x_turn', 'dst': 'game_over'},
                    {'name': 'o_wins', 'src': 'o_turn', 'dst': 'game_over'},
                    {'name': 'reset', 'src': 'game_over', 'dst': 'x_turn'},
                    {'name': 'draw', 'src': 'x_turn', 'dst': 'game_over'},
                    {'name': 'draw', 'src': 'o_turn', 'dst': 'game_over'}
                ]
            })
        elif old_cells:     # This allows us to copy boards
            self.cells = old_cells

    @property               # Returns moves that are currently possible
    def possible_moves(self):
        possible_moves = []
        for cell in self.cells:
            if self.cells[cell].state is -1:
                possible_moves.append(cell)
        return possible_moves

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
            return True, self.cells[(0, y)].state

        # check if previous move caused a win on horizontal line
        if self.cells[(x, 0)].state == self.cells[(x, 1)].state == self.cells[(x, 2)].state:
            return True, self.cells[(x, 0)].state

        # check if previous move was on the main diagonal and caused a win
        if x == y and self.cells[(0, 0)].state == self.cells[(1, 1)].state == self.cells[(2, 2)].state:
            return True, self.cells[(0, 0)].state

        # check if previous move was on the secondary diagonal and caused a win
        if x + y == 2 and self.cells[(0, 2)].state == self.cells[(1, 1)].state == self.cells[(2, 0)].state:
            return True, self.cells[(0, 2)].state

        for cell in self.cells:
            if self.cells[cell].state == -1:
                break
        else:
            return 'draw'

        return False, None


ui_frame = pygame.image.load("assets/ui_frame.png")
empty_sprite = pygame.image.load("assets/empty_sprite.png")
x_sprite = pygame.image.load("assets/x_sprite.png")
o_sprite = pygame.image.load("assets/o_sprite.png")

pygame.font.init()
game_font = pygame.font.Font("assets/m5x7.ttf", 35)

reset_button_loc = (600, 0)
reset_text_loc = (620, 35)
win_status_loc = (600, 100)
win_text_loc = (620, 135)
x_win_count_loc = (600, 200)
x_win_loc = (620, 235)
o_win_count_loc = (600, 300)
o_win_loc = (620, 335)


class BoardCell:
    def __init__(self, loc, state=None):
        if state:
            self.state = state
        else:
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
    game_surface = pygame.display.set_mode((800, 600))

    row_num = 3
    column_num = 3
    game_board = Board()

    players = (HumanPlayer('Hu'),   # X Player
               HumanPlayer("Ru")   # O Player
               )
    winner = "None"

    total_game_count = 1
    o_win_count = 0
    x_win_count = 0

    reset_game = False

    def render():
        for r in range(row_num):
            for c in range(column_num):
                cell = game_board.cells[(r, c)]
                game_surface.blit(cell.image, (cell.loc[0]*200, cell.loc[1]*200))

        game_surface.blit(ui_frame, reset_button_loc)
        reset_text = game_font.render("Reset Game", False, [0, 0, 0], None)
        game_surface.blit(reset_text, reset_text_loc)

        game_surface.blit(ui_frame, win_status_loc)
        win_text = game_font.render("Last win: "+winner, False, [0, 0, 0], None)
        game_surface.blit(win_text, win_text_loc)

        game_surface.blit(ui_frame, x_win_count_loc)
        x_win_count_text = game_font.render(players[0].name+" Wins: "+str(x_win_count), False, [0, 0, 0], None)
        game_surface.blit(x_win_count_text, x_win_loc)

        game_surface.blit(ui_frame, o_win_count_loc)
        o_win_count_text = game_font.render(players[1].name+" Wins " + str(o_win_count), False, [0, 0, 0], None)
        game_surface.blit(o_win_count_text, o_win_loc)

    while True:

        if reset_game or game_board.board_state.current == 'draw':
            total_game_count = total_game_count + 1
            reset_game = False
            game_board = Board()

        render()
        pygame.display.flip()

        if game_board.board_state.current == 'x_turn':
            move = players[0].take_turn(game_board)
            if move == 'reset':
                reset_game = True
            elif move:
                game_board.cells[move].set_x()
                win = game_board.check_win_con(move)

                if win[0]:
                    if win == 'draw':
                        game_board.board_state.trigger('draw')
                    else:
                        game_board.board_state.trigger('x_wins')
                        winner = players[0].name
                        x_win_count = x_win_count + 1

                else:
                    game_board.board_state.trigger('x_turn_taken')
            else:
                pass

        elif game_board.board_state.current == 'o_turn':
            move = players[1].take_turn(game_board)
            if move == 'reset':
                reset_game = True
            elif move:
                game_board.cells[move].set_o()
                win = game_board.check_win_con(move)
                if win[0]:
                    if win == 'draw':
                        game_board.board_state.trigger('draw')
                    else:
                        game_board.board_state.trigger('o_wins')
                        winner = players[1].name
                        o_win_count = o_win_count + 1
                else:
                    game_board.board_state.trigger('o_turn_taken')
            else:
                pass

        elif game_board.board_state.current == 'game_over':
            reset_game = True
            game_board.board_state.trigger('reset')


if __name__ == "__main__":
    main()
