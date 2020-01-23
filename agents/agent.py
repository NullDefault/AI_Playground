from abc import ABC


class Agent(ABC):

    def __init__(self, name):
        self.name = name

    def take_turn(self, game_board):

        x = 0
        y = 0

        cell_chosen_location = (x, y)

        return cell_chosen_location
