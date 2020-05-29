from random import randint
from pygame import Vector2


class Ball:
    def __init__(self, board):
        self.pos = []
        self.vel = []
        self.reset(board)
        # Effective size of the ball
        self.radius = 10

    def update_pos(self, player_paddles, board):
        self.pos = int(self.pos[0] + self.vel[0]), int(self.pos[1] + self.vel[1])
        return self.handle_collisions(player_paddles, board)

    def reset(self, board):
        self.pos = board.center
        x_dir = -4 if randint(0, 1) == 0 else 4
        self.vel = [x_dir, randint(-4, 4)]

    def handle_collisions(self, paddles, board):
        # ball collision check on top and bottom walls
        if int(self.pos[1]) <= self.radius:
            self.pos = (self.pos[0], self.radius)
            self.vel[1] = -self.vel[1]

        elif int(self.pos[1]) >= board.height + 1 - self.radius:
            self.pos = (self.pos[0], board.height - self.radius)
            self.vel[1] = -self.vel[1]

        # collide with left paddle
        if paddles[0].rect.collidepoint(self.pos[0] - self.radius, self.pos[1]):
            self.vel[0] = -self.vel[0]
        # collide with right paddle
        elif paddles[1].rect.collidepoint(self.pos[0] + self.radius, self.pos[1]):
            self.vel[0] = -self.vel[0]

        if self.pos[0] < 0:
            self.reset(board)
            return [0, 1]

        elif self.pos[0] > board.width:
            self.reset(board)
            return [1, 0]

