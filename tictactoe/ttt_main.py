import pygame
import numpy as np
from fysom import Fysom
from matplotlib import pyplot as plt

from tictactoe.agents.ttt_agents.qn_agent import QNAgent
from tictactoe.agents.ttt_agents.random_agent import RandomAgent


class Board:
    def __init__(self, old_cells=None):
        if old_cells is None:
            self.cells = self.init_cells(3)
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

    def init_cells(self, size):
        return np.full(shape=(size, size), fill_value=-1)

    def check_win_con(self, last_move):
        x = last_move[0]
        y = last_move[1]

        # check if previous move caused a win on vertical line
        if self.cells[(0, y)] == self.cells[(1, y)] == self.cells[(2, y)]:
            return True

        # check if previous move caused a win on horizontal line
        if self.cells[(x, 0)] == self.cells[(x, 1)] == self.cells[(x, 2)]:
            return True

        # check if previous move was on the main diagonal and caused a win
        if x == y and self.cells[(0, 0)] == self.cells[(1, 1)] == self.cells[(2, 2)]:
            return True

        # check if previous move was on the secondary diagonal and caused a win
        if x + y == 2 and self.cells[(0, 2)] == self.cells[(1, 1)] == self.cells[(2, 0)]:
            return True

        for r in range(3):
            for c in range(3):
                if self.cells[(r, c)] == -1:
                    return False
        return "draw"


ui_frame = pygame.image.load("assets/ttt_assets/ui_frame.png")
empty_sprite = pygame.image.load("assets/ttt_assets/empty_sprite.png")
bg_img = pygame.image.load("assets/ttt_assets/bg_img.png")
x_sprite = pygame.image.load("assets/ttt_assets/x_sprite.png")
o_sprite = pygame.image.load("assets/ttt_assets/o_sprite.png")

pygame.font.init()
game_font = pygame.font.Font("assets/m5x7.ttf", 35)
SHOW_EVERY = 1
MAX_GAMES = 25000

reset_button_loc = (600, 0)
reset_text_loc = (620, 35)
win_status_loc = (600, 100)
win_text_loc = (620, 135)
x_win_count_loc = (600, 200)
x_win_loc = (620, 235)
o_win_count_loc = (600, 300)
o_win_loc = (620, 335)
bg_loc = (600, 400)


def main():
    game_surface = pygame.display.set_mode((800, 600))

    row_num = 3
    column_num = 3
    game_board = Board()

    players = (RandomAgent('DQN'),  # X Player
               RandomAgent('Random'),  # O Player
               )
    winner = "None"

    x_wins = []
    o_wins = []

    total_game_count = 0
    o_win_count = 0
    x_win_count = 0

    reset_game = False

    def reset_game_for_qnas():
        if isinstance(players[0], QNAgent):
            players[0].new_game()
        if isinstance(players[1], QNAgent):
            players[1].new_game()

    def render():
        for r in range(row_num):
            for c in range(column_num):
                state = game_board.cells[(c, r)]
                if state == 1:
                    sprite = x_sprite
                elif state == 0:
                    sprite = o_sprite
                else:
                    sprite = empty_sprite
                game_surface.blit(sprite, (c*200, r*200))

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

        game_surface.blit(bg_img, bg_loc)

    while total_game_count < MAX_GAMES:
        if reset_game or game_board.board_state.current == 'draw':
            total_game_count = total_game_count + 1

            if total_game_count == MAX_GAMES:
                plt.plot(range(0, MAX_GAMES-1), x_wins, 'x', linestyle='dashed')
                plt.plot(range(0, MAX_GAMES-1), o_wins, '.', linestyle='dashed')
                plt.show()

                quit()

            print(total_game_count)
            x_wins.append(x_win_count)
            o_wins.append(o_win_count)
            reset_game = False
            game_board = Board()
            reset_game_for_qnas()

        render()
        pygame.display.update()

        if game_board.board_state.current == 'x_turn':
            move = players[0].take_turn(game_board)
            if move == 'reset':
                reset_game = True
            elif move:
                game_board.cells[move] = 1
                win = game_board.check_win_con(move)

                if win:
                    if win == 'draw':
                        game_board.board_state.trigger('draw')
                        if isinstance(players[0], QNAgent):
                            players[0].reward(-1)
                        if isinstance(players[1], QNAgent):
                            players[1].reward(-1)
                    else:
                        game_board.board_state.trigger('x_wins')
                        winner = players[0].name
                        x_win_count = x_win_count + 1

                        if isinstance(players[0], QNAgent):
                            players[0].reward(+1)
                        if isinstance(players[1], QNAgent):
                            players[1].reward(-1)

                else:
                    game_board.board_state.trigger('x_turn_taken')
            else:
                continue

        elif game_board.board_state.current == 'o_turn':
            move = players[1].take_turn(game_board)
            if move == 'reset':
                reset_game = True
            elif move:
                game_board.cells[move] = 0
                win = game_board.check_win_con(move)
                if win:
                    if win == 'draw':
                        game_board.board_state.trigger('draw')
                        if isinstance(players[0], QNAgent):
                            players[0].reward(-0.5)
                        if isinstance(players[1], QNAgent):
                            players[1].reward(-0.5)
                    else:
                        game_board.board_state.trigger('o_wins')
                        winner = players[1].name
                        o_win_count = o_win_count + 1

                        if isinstance(players[1], QNAgent):
                            players[1].reward(+1)
                        if isinstance(players[0], QNAgent):
                            players[0].reward(-1)
                else:
                    game_board.board_state.trigger('o_turn_taken')
            else:
                continue

        elif game_board.board_state.current == 'game_over':
            reset_game = True
            game_board.board_state.trigger('reset')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break


if __name__ == "__main__":
    main()
