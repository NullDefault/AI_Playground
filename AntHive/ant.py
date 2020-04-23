from random import randint
from pygame import Vector2
from math import atan2, pi


def make_path():
    path_len = 10
    path = [None for i in range(path_len)]
    for i in range(path_len):
        path[i] = randint(-1, 4), randint(2, 3)
    return path


class Ant:
    def __init__(self, location):
        self.angle = randint(0, 360)
        self.loc = Vector2(location)
        self.path = make_path()
        self.path_index = 0

    def update(self, target_surf, x_offset, y_offset):
        self.path_index += 1
        if self.path_index > len(self.path)-1:
            self.path_index = 0

        old_x = self.loc.x
        old_y = self.loc.y

        self.loc.x += self.path[self.path_index][0]
        self.loc.y += self.path[self.path_index][1]

        if not self.check_edges(target_surf, x_offset, y_offset):
            self.loc.x = old_x
            self.loc.y = old_y

        self.angle = 270 - atan2(self.loc.y - old_y, self.loc.x - old_x) * 180 / pi

    def check_edges(self, surface, x_offset, y_offset):
        try:
            dest_col = surface.get_at((int(self.loc.x-x_offset), int(self.loc.y-y_offset)))
        except IndexError:
            # Unsure how to get around this yet, might have to change approach
            return True
        if dest_col != (170, 146, 85, 255):
            return False
        else:
            return True

