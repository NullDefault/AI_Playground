import pygame as pg
from random import randint

pg.init()

screen_width = 1000
screen_height = 500


class Ball:
    def __init__(self):
        self.pos = (screen_width // 2, screen_height // 2)
        self.vel = (randint(-10, 10), randint(-10, 10))
        self.color = (0, 255, 0)

    def update_pos(self):
        self.check_bounds()
        self.vel = self.vel[0], self.vel[1]
        self.pos = (int(self.pos[0] + self.vel[0]), int(self.pos[1] + self.vel[1]))

    def check_bounds(self, players):
        if self.pos[0] < 0:
            self.vel = -self.vel[0], self.vel[1]
        elif self.pos[0] > screen_width:
            self.vel = -self.vel[0], self.vel[1]
        elif self.pos[1] < 0:
            self.vel = self.vel[0], -self.vel[1]
            print("down")
        elif self.pos[1] > screen_height:
            self.vel = self.vel[0], -self.vel[1]
            print("up")


screen = pg.display.set_mode((screen_width, screen_height))
clock = pg.time.Clock()

ball = Ball()
players = [pg.Rect(50, screen_height / 2 - 50, 12, 100), pg.Rect(screen_width - 50, screen_height / 2 - 50, 12, 100)]
done = False


def render():
    screen.fill((0, 0, 0))
    for player in players:
        pg.draw.rect(screen, (255, 255, 255), player)

    # draw dividing line
    pg.draw.line(screen, (255, 0, 0), (screen_width / 2, 0), (screen_width / 2, screen_height), 1)

    # draw ball
    ball.update_pos()
    pg.draw.circle(screen, ball.color, ball.pos, 10)


while not done:
    clock.tick(60)
    render()

    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
            pg.quit()



