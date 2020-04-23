import pygame

from AntHive.map import Map

map_dims = (1000, 500)
frame_size = (1600, 800)
s = 10
game_map = Map(map_dims[0], map_dims[1], s)
surf = pygame.display.set_mode(frame_size)


x_offset = 0
y_offset = 0

running = True
while running:
    map_surf = game_map.render()
    map_surf = pygame.transform.scale(map_surf, (map_dims[0]*4, map_dims[1]*4))
    surf.blit(map_surf, dest=(0, 0), area=pygame.Rect(0+x_offset, 0+y_offset, frame_size[0], frame_size[1]))
    print(x_offset)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            print(y_offset)
            if key == 'w' or key == 'up':
                y_offset = y_offset - 100
                if y_offset < 0:
                    y_offset = 0
            elif key == 's' or key == 'down':
                y_offset = y_offset + 100
                if y_offset > map_dims[1]*4 - frame_size[1]:
                    y_offset = y_offset - 100

            elif key == 'd' or key == 'right':
                x_offset = x_offset + 100
                if x_offset > map_dims[0]*4 - frame_size[0]:
                    x_offset = x_offset - 100

            elif key == 'a' or key == 'left':
                x_offset = x_offset - 100
                if x_offset < 0:
                    x_offset = 0
    pygame.display.update()
pygame.quit()
