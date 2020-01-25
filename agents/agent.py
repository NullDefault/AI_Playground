'''
Abstract Class representing an individual agent. Every agent has an identifying name and a function that lets them
take a turn on the game board.
'''

from abc import ABC


class Agent(ABC):

    def __init__(self, name):
        self.name = name

    def take_turn(self, game_board):

        x = 0   # Row
        y = 0   # Column

        cell_chosen_location = (x, y)

        return cell_chosen_location
