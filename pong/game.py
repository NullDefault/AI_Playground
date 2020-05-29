from pong.ball import Ball
from pong.paddle import Paddle
from pygame import Rect, draw, font

from pong.paddle_controllers.aimbot import AimBot
from pong.paddle_controllers.random import Random

WHITE = (255, 255, 255)
BLACK = (0,     0,   0)
BLUE  = (0,     0, 255)
RED   = (255,   0,   0)
GREEN = (0,   255,   0)

font.init()
game_font = font.SysFont("Comic Sans MS", 20)

aimbot = AimBot()
random = Random()


class Game:
    def __init__(self):
        self.board = Rect((0, 0), (1000, 500))
        self.paddles = [Paddle(True, self.board, aimbot), Paddle(False, self.board, aimbot)]
        self.ball = Ball(self.board)
        self.scores = [0, 0]

    def next_frame(self):
        for paddle in self.paddles:
            paddle.move(self.ball)

        score_change = self.ball.update_pos(self.paddles, self.board)

        if score_change:
            self.scores[0] = score_change[0] + self.scores[0]
            self.scores[1] = score_change[1] + self.scores[1]

    def render(self, screen):
        # Draw board
        draw.rect(screen, BLACK, self.board)

        # Paint left paddle
        draw.rect(screen, BLUE, self.paddles[0].rect)
        # Paint right paddle
        draw.rect(screen, RED, self.paddles[1].rect)

        # Draw ball
        draw.circle(screen, WHITE, self.ball.pos, self.ball.radius)

        # Draw score
        score_left = game_font.render(str(self.scores[0]), 1, GREEN)
        score_right = game_font.render(str(self.scores[1]), 1, GREEN)
        screen.blit(score_left, (self.board.w // 2 - 45, 50))
        screen.blit(score_right, (self.board.w // 2 + 30, 50))

        # Draw dividing line
        draw.line(screen, WHITE, (self.board.w // 2, 0), (self.board.w // 2, self.board.h))


