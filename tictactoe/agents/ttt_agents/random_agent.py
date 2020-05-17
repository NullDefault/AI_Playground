'''
This agent just randomly picks an open cell when its their turn to make a move
'''

from tictactoe.agents.ttt_agents.agent import Agent
import random


class RandomAgent(Agent):

    def __init__(self, name):
        Agent.__init__(self, name)

    def take_turn(self, game_board):
        turn_choice = None
        while turn_choice is None:

            x = random.randint(0, 2)
            y = random.randint(0, 2)
            turn_choice = x, y

            if game_board.cells[(x, y)] != -1:
                turn_choice = None

        return turn_choice


