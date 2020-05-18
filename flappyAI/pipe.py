from os.path import join
from random import randrange

from pygame.mask import from_surface
from pygame.transform import flip

from flappyAI.shared_logic import load


class Pipe:
    IMG = load(join("assets", "pipe.png"))
    GAP = 200
    V = 5  # velocity

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bot = 0

        self.PIPE_TOP = flip(self.IMG, False, True)
        self.PIPE_BOT = self.IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bot = self.height + self.GAP

    def move(self):
        self.x -= self.V

    def render(self, surf):
        surf.blit(self.PIPE_TOP, (self.x, self.top))
        surf.blit(self.PIPE_BOT, (self.x, self.bot))

    def collides_with(self, bird):
        bird_mask = bird.get_mask()
        top_mask = from_surface(self.PIPE_TOP)
        bot_mask = from_surface(self.PIPE_BOT)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bot_offset = (self.x - bird.x, self.bot - round(bird.y))

        top_collision = bird_mask.overlap(top_mask, top_offset)
        bot_collision = bird_mask.overlap(bot_mask, bot_offset)

        if top_collision or bot_collision:
            return True
        else:
            return False
