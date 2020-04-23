import pygame
from os.path import join
from AntHive.logic_functions import process_key, process_mouse
from AntHive.map import Map
from random import randint

map_dims = (1000, 500)
frame_size = (1600, 900)
s = 7
game_map = Map(map_dims[0], map_dims[1], s)
surf = pygame.display.set_mode(frame_size)
ant_sprite = pygame.image.load(join("sprites", "ant.png"))
ants = []

x_offset = 0
y_offset = 0

drag_begin = None

running = True
while running:
    map_surf = game_map.render()
    map_surf = pygame.transform.scale(map_surf, (map_dims[0]*s, map_dims[1]*s))
    surf.blit(map_surf, dest=(0, 0), area=pygame.Rect(0+x_offset, 0+y_offset, frame_size[0], frame_size[1]))
    for ant in ants:
        ant.update(surf, x_offset, y_offset)
        if (x_offset <= ant.loc.x <= x_offset+frame_size[0]) and (y_offset <= ant.loc.y <= y_offset+frame_size[1]):
            temp = ant_sprite.copy()
            temp = pygame.transform.rotate(temp, ant.angle)
            surf.blit(temp, (int(ant.loc.x-x_offset), int(ant.loc.y-y_offset)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            x_offset, y_offset = process_key(key, x_offset, y_offset, s)
        else:
            drag_begin, x_offset, y_offset, ants = process_mouse(
                x_offset, y_offset, drag_begin, event, ants, map_dims, frame_size, s)
    pygame.display.update()
pygame.quit()

