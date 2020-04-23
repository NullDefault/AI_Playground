import pygame

from AntHive.ant import Ant
from AntHive.map import Map

map_dims = (1000, 500)
frame_size = (1800, 1000)
s = 10
game_map = Map(map_dims[0], map_dims[1], s)
surf = pygame.display.set_mode(frame_size)
ants = pygame.sprite.RenderUpdates()

def check_camera_edges(x_off, y_off):
    if y_off < 0:
        y_off = 0
    if y_off > map_dims[1] * 4 - frame_size[1]:
        y_off = map_dims[1] * 4 - frame_size[1]
    if x_off > map_dims[0] * 4 - frame_size[0]:
        x_off = map_dims[0] * 4 - frame_size[0]
    if x_off < 0:
        x_off = 0

    return x_off, y_off


def process_key(k, x_off, y_off):
    if k == 'w' or k == 'up':
        y_off = y_off - 100
    elif k == 's' or k == 'down':
        y_off = y_off + 100
    elif k == 'd' or k == 'right':
        x_off = x_off + 100
    elif k == 'a' or k == 'left':
        x_off = x_off - 100

    return check_camera_edges(x_off, y_off)


def process_mouse(x_off, y_off, drag_a):
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            drag_b = pygame.Vector2(event.pos)
            drag_direction = drag_a - drag_b
            x_off = int(x_off + drag_direction[0])
            y_off = int(y_off + drag_direction[1])

    elif event.type == pygame.MOUSEBUTTONDOWN:
        print(event.button)
        if event.button == 1:
            mouse_x, mouse_y = event.pos
            drag_a = pygame.Vector2(mouse_x, mouse_y)
        elif event.button == 3:
            ants.add(Ant(event.pos))

    offs = check_camera_edges(x_off, y_off)
    return drag_a, offs[0], offs[1]


x_offset = 0
y_offset = 0

drag_begin = None

running = True
while running:
    map_surf = game_map.render()
    map_surf = pygame.transform.scale(map_surf, (map_dims[0]*4, map_dims[1]*4))
    surf.blit(map_surf, dest=(0, 0), area=pygame.Rect(0+x_offset, 0+y_offset, frame_size[0], frame_size[1]))
    ants.draw(surf)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            x_offset, y_offset = process_key(key, x_offset, y_offset)
        else:
            drag_begin, x_offset, y_offset = process_mouse(x_offset, y_offset, drag_begin)
    pygame.display.update()
pygame.quit()

