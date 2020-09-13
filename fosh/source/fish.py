from fosh.source.fish_components.locomotion import Locomotion
from fosh.source.fish_components.fish_component import FishComponent
import pygame as pg


class FishSurface(FishComponent):
    def __init__(self, fish):
        super().__init__(fish)
        size = 100*self.host.size, 50*self.host.size
        self.sprite = pg.Surface(size)
        self.sprite.set_colorkey((0, 0, 0))

        self.mouth_point = [0, size[1] // 2]
        self.bottom = [size[0] // 3, self.mouth_point[1] + 20]
        self.top = [size[0] // 3, self.mouth_point[1] - 20]
        self.tail_point = [size[0] // 3 * 2, size[1] // 2]

        pg.draw.polygon(self.sprite, (249, 245, 100), [self.top, [self.top[0] + 10, self.top[1] - 7], [self.bottom[0] + 10, self.bottom[1] + 7], self.bottom])

        pg.draw.polygon(self.sprite, (255, 0, 0), [self.mouth_point,
                                                   self.bottom, self.tail_point,
                                                   self.top])
        pg.draw.polygon(self.sprite, (255, 0, 0), [self.tail_point,
                                                   [size[0], self.top[1] + 7],
                                                   [size[0], self.bottom[1] - 7]])


class Fish:
    def __init__(self, screen_size):
        # self.dna = DNA()
        # self.stomach = Stomach()
        self.locomotion = Locomotion(self, [screen_size[0]//2, screen_size[1]//2])
        self.size = 1
        self.surface = FishSurface(self)
