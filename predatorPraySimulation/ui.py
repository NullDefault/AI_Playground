import pygame as pg
from numpy import nditer

from predatorPraySimulation.constants import *


def render(render_surface, canvas, tiles, size, offset):
    with nditer(tiles, flags=['multi_index']) as it:
        for tile in it:
            if bool(tile['fox']) is True:
                color = COLORS['fox']
            elif bool(tile['rabbit']) is True:
                color = COLORS['rabbit']
            else:
                color = COLORS['grass_colors'][int(tile['grass'])]
            tile_index = it.multi_index
            pg.draw.rect(render_surface, color,
                         pg.Rect(tile_index[0] * size + offset * tile_index[0] + 5,
                                 tile_index[1] * size + offset * tile_index[1] + 5,
                                 size, size))

    return canvas.blit(render_surface, (0, 0))
