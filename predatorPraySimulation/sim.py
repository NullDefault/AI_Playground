import pygame as pg
import pygame_gui as pgui

from predatorPraySimulation.constants import *
from predatorPraySimulation.data import init_tiles
from predatorPraySimulation.ui import render

pg.init()
canvas = pg.display.set_mode((WIDTH, HEIGHT))
render_surface = pg.Surface((WIDTH, HEIGHT))
render_surface = render_surface.convert_alpha()
render_surface.fill(COLORS['brown'])
clock = pg.time.Clock()
ui_manager = pgui.UIManager((WIDTH, HEIGHT))


def main():
    running = True
    chosen_size = 'medium'
    tiles = init_tiles(chosen_size)

    iteration = 0
    render_interval = 50

    while running:
        time_delta = clock.tick(60) / 1000.0
        pg.display.set_caption("FPS: " + str(int(clock.get_fps())) + "      Iteration: " + str(iteration))
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            if event.type == pg.USEREVENT:
                if event.user_type == 'ui_button_pressed':
                    pass

            ui_manager.process_events(event)

        ui_manager.update(time_delta)
        if iteration % render_interval == 0:
            pg.display.update(render(render_surface, canvas, tiles, SIZES[chosen_size][1], SIZES[chosen_size][2]))
        iteration = iteration + 1


if __name__ == "__main__":
    main()
