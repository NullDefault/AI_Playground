from flappyAI.shared_logic import load
from os.path import join


class Base:
    V = 5
    SPRITE = load(join("assets", "base.png"))
    WIDTH = SPRITE.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.V
        self.x2 -= self.V

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def render(self, surf):
        surf.blit(self.SPRITE, (self.x1, self.y))
        surf.blit(self.SPRITE, (self.x2, self.y))

