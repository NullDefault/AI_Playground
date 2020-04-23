from pygame.sprite import DirtySprite
from pygame import image, transform
from os.path import join
from random import randint


class Ant(DirtySprite):
    def __init__(self, location):
        self.image = image.load(join('sprites', 'ant.png'))
        angle = randint(0, 360)
        self.image = transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        DirtySprite.__init__(self)
