import numpy as np
import pygame


def neighbors(data, i, j, d):
    n = data[i - d:i + d + 1, j - d:j + d + 1].flatten()
    return n


def count(l):
    c = 0
    for val in l:
        if val == 1:
            c += 1
    return c


def gen_step(dim, init_data, a, b, steps):
    for i in range(steps):
        if i == 0:
            data = np.zeros(dim)
        for x in range(dim[0]):
            for y in range(dim[1]):
                d_1 = neighbors(init_data, x, y, 1)
                d_2 = neighbors(init_data, x, y, 2)
                if count(d_1) >= a:
                    data[x][y] = 1
                elif count(d_2) <= b:
                    data[x][y] = 1
                else:
                    data[x][y] = 0

    return data


def generate_map(xd, yd, scale):
    dim = (xd//scale, yd//scale)
    init_data = np.random.random(dim)

    # Make the initial array
    with np.nditer(init_data, op_flags=['readwrite']) as it:
        for val in it:
            if val < 0.5:
                val[...] = 0
            else:
                val[...] = 1

    # Run generation steps
    init_data = gen_step(dim, init_data, a=5, b=2, steps=2)
    init_data = gen_step(dim, init_data, a=4, b=-1, steps=5)

    # Color walls
    for x in range(dim[0]):
        for y in range(dim[1]):
            if init_data[x][y] == 1:
                x_moves = (-1, 1, 0, 0)
                y_moves = (0, 0, 1, -1)
                for i in range(4):
                    x_m = x_moves[i]
                    y_m = y_moves[i]
                    try:
                        if init_data[x+x_m][y+y_m] == 0:
                            init_data[x+x_m][y+y_m] = 255
                    except IndexError:
                        pass

    # Clean up the edges
    init_data[0:][0] = 255
    init_data[dim[0]-1][0:] = 255
    for i in range(dim[0]):
        init_data[i][dim[1]-1] = 255

    return init_data


class Map:
    def __init__(self, x_dim, y_dim, scale):
        self.map_data = generate_map(x_dim, y_dim, scale)

    def render(self, dimensions):
        ms = pygame.surfarray.make_surface(self.map_data)
        ms = pygame.transform.scale(ms, dimensions)
        pygame.PixelArray(ms).replace(255, (15, 163, 64))
        pygame.PixelArray(ms).replace((0, 0, 85, 255), (166, 162, 116))
        return ms


dimensions = (1600, 800)
s = 10
map = Map(dimensions[0], dimensions[1], s)
surf = pygame.display.set_mode((dimensions[0]+100, dimensions[1]+100))


running = True
while running:
    map_surf = map.render(dimensions)
    surf.blit(map_surf, (50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()
