import pygame as pg

from pong.game import Game

pg.init()

screen = pg.display.set_mode((1000, 500))
clock = pg.time.Clock()
done = False

game = Game()

while not done:
    clock.tick(60)
    pg.display.flip()

    game.next_frame()
    game.render(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
            pg.quit()



