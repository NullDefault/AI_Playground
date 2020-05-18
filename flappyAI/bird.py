from os.path import join

from pygame.mask import from_surface
from pygame.transform import rotate

from flappyAI.shared_logic import load


class Bird:
    SPRITES = [load(join("assets", "bird1.png")),
               load(join("assets", "bird2.png")),
               load(join("assets", "bird3.png"))]
    MAX_ROT = 25  # max rotation
    ROT_VEL = 20  # rotation velocity
    ANIM_TIME = 5  # animation time

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = self.y

        self.tilt = 0
        self.tick = 0
        self.v = 0  # velocity
        self.frame = 0

        self.sprite = self.SPRITES[self.frame]

    def jump(self):
        self.v = -10.5
        self.tick = 0
        self.height = self.y

    def move(self):
        self.tick += 1

        # for downward acceleration
        d = self.v * self.tick + 0.5 * 3 * self.tick ** 2  # calculate displacement

        # terminal velocity
        if d >= 16:
            d = (d / abs(d)) * 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def render(self, surf):
        self.frame += 1

        # For animation of bird, loop through three images
        if self.frame <= self.ANIM_TIME:
            self.sprite = self.SPRITES[0]
        elif self.frame <= self.ANIM_TIME * 2:
            self.sprite = self.SPRITES[1]
        elif self.frame <= self.ANIM_TIME * 3:
            self.sprite = self.SPRITES[2]
        elif self.frame <= self.ANIM_TIME * 4:
            self.sprite = self.SPRITES[1]
        elif self.frame == self.ANIM_TIME * 4 + 1:
            self.sprite = self.SPRITES[0]
            self.frame = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.sprite = self.SPRITES[1]
            self.frame = self.ANIM_TIME * 2

        # tilt the bird
        rotated_sprite = rotate(self.sprite, self.tilt)
        new_rect = rotated_sprite.get_rect(center=self.sprite.get_rect(topleft=(self.x, self.y)).center)
        surf.blit(rotated_sprite, new_rect.topleft)

    def get_mask(self):
        return from_surface(self.sprite)
