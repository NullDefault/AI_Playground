import numpy as np
import pygame as pg
import pygame_gui as pgui
from random import randint

WIDTH, HEIGHT = 1280, 920
SIZES = {
    'small': [50, 10, 6],
    'medium': [100, 5, 3],
    'large': [125, 4, 2.4],
    'too big': [250, 2, 1.2]
}

COLORS = {
    'fox':    pg.Color(255, 150, 50),
    'rabbit': pg.Color(50, 25, 0),
    'brown':  pg.Color(150, 100, 45),
    'grass_colors': {
        0: pg.Color(230, 255, 240),
        1: pg.Color(200, 255, 200),
        2: pg.Color(145, 255, 110),
        3: pg.Color(100, 255, 80),
        4: pg.Color(60, 255, 40),
        5: pg.Color(40, 255, 20),
        6: pg.Color(15, 255, 10)
    }
}

pg.init()
canvas = pg.display.set_mode((WIDTH, HEIGHT))
render_surface = pg.Surface((WIDTH, HEIGHT))
render_surface = render_surface.convert_alpha()
render_surface.fill(COLORS['brown'])
clock = pg.time.Clock()
ui_manager = pgui.UIManager((WIDTH, HEIGHT))


def init_tiles(chosen_size):
    chosen_size = SIZES[chosen_size][0]
    arr = np.zeros([chosen_size, chosen_size], np.dtype([('rabbit', np.bool), ('fox', np.bool), ('grass', np.int)]))

    with np.nditer(arr, op_flags=['readwrite']) as it:
        for x in it:
            r = randint(0, 10)
            if r == 0:
                x['rabbit'] = True
            f = randint(0, 50)
            if f == 0:
                x['fox'] = True
            x['grass'] = randint(0, 6)
    return arr


def render(tiles, size, offset):
    with np.nditer(tiles, flags=['multi_index']) as it:
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


def main():
    running = True
    chosen_size = 'medium'
    tiles = init_tiles(chosen_size)

    iteration = 0
    render_interval = 50

    while running:
        time_delta = clock.tick(60) / 1000.0
        pg.display.set_caption("FPS: " + str(int(clock.get_fps())) + "      Iteration: "+str(iteration))
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            if event.type == pg.USEREVENT:
                if event.user_type == 'ui_button_pressed':
                    pass

            ui_manager.process_events(event)

        ui_manager.update(time_delta)
        if iteration % render_interval == 0:
            pg.display.update(render(tiles, SIZES[chosen_size][1], SIZES[chosen_size][2]))
        iteration = iteration + 1


if __name__ == "__main__":
    main()
