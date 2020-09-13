"""
Code is adapted from NEAT flappy bird tutorial by tech with tim
@https://github.com/techwithtim/NEAT-Flappy-Bird/blob/master/flappy_bird.py
"""
import pygame as pg
import neat

WIDTH = 550
HEIGHT = 800
screen = pg.display.set_mode((WIDTH, HEIGHT))

from os.path import join, dirname
from random import randint
from flappyAI.shared_logic import load
from flappyAI.bird import Bird
from flappyAI.pipe import Pipe
from flappyAI.base import Base

BG = load(join("assets", "bg.png"))


def render_frame(surf, birds, pipes, base):
    surf.blit(BG, (0, 0))

    for p in pipes:
        p.render(surf)

    base.render(surf)

    for bird in birds:
        bird.render(surf)

    pg.display.update()


def update_state(birds, pipes, base, score, genes, nets):
    base.move()

    pipe_ix = 0
    if len(birds) > 0:
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ix = 1
    else:
        return True, score

    for x, bird in enumerate(birds):
        bird.move()
        genes[x].fitness += 0.01

        output = nets[x].activate((bird.y,
                                   abs(bird.y - pipes[pipe_ix].HEIGHT),
                                   abs(bird.y - pipes[pipe_ix].bot)))

        if output[0] > 0.5:
            bird.jump()

    pipes_to_remove = []
    add_pipe = False
    for pipe in pipes:

        for x, bird in enumerate(birds):
            if pipe.collides_with(bird):
                genes[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                genes.pop(x)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            pipes_to_remove.append(pipe)

        pipe.move()

    if add_pipe:
        score += 1
        for g in genes:
            g.fitness += 3
        pipes.append(Pipe(WIDTH+100 - randint(0, 100)))

    for pipe in pipes_to_remove:
        pipes.remove(pipe)

    for x, bird in enumerate(birds):
        if bird.y + bird.sprite.get_height() >= 730 or bird.y < 0:
            birds.pop(x)
            nets.pop(x)
            genes.pop(x)

    return False, score


def run_game(genomes, config):
    score = 0

    birds = []
    genes = []
    nets = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        genes.append(g)

    pipes = [Pipe(WIDTH)]

    base = Base(HEIGHT - 70)

    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(600)
        pg.display.set_caption("Flappy AI   FPS:"+str(int(clock.get_fps()))+"    SCORE:"+str(score))

        stop, score = update_state(birds, pipes, base, score, genes, nets)
        if stop:
            break
        render_frame(screen, birds, pipes, base)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()


def run_neat(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(run_game, 50)


def main():
    local_dir = dirname(__file__)
    config_path = join(local_dir, 'config-feedforward.txt')
    run_neat(config_path)


if __name__ == "__main__":
    main()
