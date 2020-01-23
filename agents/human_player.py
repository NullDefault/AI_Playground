from agents.agent import Agent
from pygame import event, MOUSEBUTTONUP, mouse


class HumanPlayer(Agent):

    def __init__(self, team):
        Agent.__init__(self, team)

    def take_turn(self, game_board):
        turn_choice = None
        while turn_choice is None:
            for e in event.get():
                if e.type == MOUSEBUTTONUP:
                    x = None
                    y = None

                    pos = mouse.get_pos()

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

        return turn_choice
