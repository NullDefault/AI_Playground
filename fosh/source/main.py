import pygame as pg
import pygame_gui as pgui
import numpy as np
from fosh.source.fish import Fish
from fosh.source.environment import Environment

WIDTH = 1200
HEIGHT = 800
LIGHT_BLUE = (0, 173, 249)
BLUE = (0, 89, 255)
SAND = (221, 214, 140)
WALL = (189, 219, 225)
WALL_B = (162, 191, 198)
F_PANEL = (124, 147, 156)

pg.init()
canvas = pg.display.set_mode((WIDTH, HEIGHT))
render_surface = pg.Surface((WIDTH, HEIGHT))
render_surface = render_surface.convert_alpha()
render_surface.fill(pg.Color(0))
clock = pg.time.Clock()
ui_manager = pgui.UIManager((WIDTH, HEIGHT))


def render(env, f):
    surface_layer = pg.Surface((WIDTH, HEIGHT))
    surface_layer.set_colorkey((0, 0, 0))
    surface_layer.set_alpha(50)

    pg.draw.polygon(surface_layer, WALL, env.l_wall)
    pg.draw.polygon(surface_layer, WALL, env.r_wall)
    pg.draw.polygon(surface_layer, WALL_B, env.b_wall)
    pg.draw.polygon(surface_layer, SAND, env.floor_coords)

    water_layer = pg.Surface((WIDTH, HEIGHT))
    water_layer.set_colorkey((0, 0, 0))
    water_layer.set_alpha(100)
    pg.draw.polygon(water_layer, BLUE, env.water)
    pg.draw.polygon(water_layer, LIGHT_BLUE, env.water_cap)

    surface_layer.blit(water_layer, (0, 0))
    render_surface.blit(surface_layer, (0, 0))
    pg.draw.polygon(render_surface, F_PANEL, env.f_panel, 10)

    for fish in f:
        render_surface.blit(fish.surface.sprite, fish.locomotion.xy)

    canvas.blit(render_surface, (0, 0))


def main():
    running = True
    fish = [Fish((WIDTH, HEIGHT))]
    environment = Environment(w=WIDTH, h=HEIGHT)

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            if event.type == pg.USEREVENT:
                if event.user_type == 'ui_button_pressed':
                    pass

            ui_manager.process_events(event)

        ui_manager.update(time_delta)
        render(environment, fish)
        pg.display.update()


if __name__ == "__main__":
    main()
