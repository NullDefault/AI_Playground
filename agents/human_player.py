from agents.agent import Agent
from pygame import event, MOUSEBUTTONUP, mouse


class HumanPlayer(Agent):

    def __init__(self, name):
        Agent.__init__(self, name)

    def take_turn(self, game_board):
        turn_choice = None
        while turn_choice is None:
            for e in event.get():
                if e.type == MOUSEBUTTONUP:
                    x = None
                    y = None

                    pos = mouse.get_pos()

                    if pos[0] > 600 and pos[1] <= 100:
                        return 'reset'

                    if 0 <= pos[0] <= 200:
                        x = 0
                    elif 201 <= pos[0] <= 400:
                        x = 1
                    elif 401 <= pos[0] <= 600:
                        x = 2

                    if 0 <= pos[1] <= 200:
                        y = 0
                    elif 201 <= pos[1] <= 400:
                        y = 1
                    elif 401 <= pos[1] <= 600:
                        y = 2

                    turn_choice = x, y

                    if x is None or y is None or game_board.cells[(x, y)].state is not -1:
                        turn_choice = None


        return turn_choice
