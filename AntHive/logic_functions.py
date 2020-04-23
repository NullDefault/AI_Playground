import pygame
from AntHive.ant import Ant


def check_camera_edges(x_off, y_off, map_dims, frame_size, s):
    if y_off < 0:
        y_off = 0
    if y_off > map_dims[1] * s - frame_size[1]:
        y_off = map_dims[1] * s - frame_size[1]
    if x_off > map_dims[0] * s - frame_size[0]:
        x_off = map_dims[0] * s - frame_size[0]
    if x_off < 0:
        x_off = 0

    return x_off, y_off


def process_key(k, x_off, y_off, scale):
    if k == 'w' or k == 'up':
        y_off = y_off - 100
    elif k == 's' or k == 'down':
        y_off = y_off + 100
    elif k == 'd' or k == 'right':
        x_off = x_off + 100
    elif k == 'a' or k == 'left':
        x_off = x_off - 100

    return check_camera_edges(x_off, y_off, scale)


def process_mouse(x_off, y_off, drag_a, event, ants, map_dims, frame_size, scale):
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            drag_b = pygame.Vector2(event.pos)
            drag_direction = drag_a - drag_b
            x_off = int(x_off + drag_direction[0])
            y_off = int(y_off + drag_direction[1])

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            mouse_x, mouse_y = event.pos
            drag_a = pygame.Vector2(mouse_x, mouse_y)
        elif event.button == 3:
            ants.append(Ant((int(event.pos[0]+x_off), int(event.pos[1]+y_off))))

    offs = check_camera_edges(x_off, y_off, map_dims, frame_size, scale)
    return drag_a, offs[0], offs[1], ants
