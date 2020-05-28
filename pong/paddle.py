from pygame import Rect
from random import randint


class Paddle:
    def __init__(self, left, board):

        paddle_height = 70
        paddle_width = 100

        if left:
            self.rect = Rect(paddle_width, board.centery - paddle_height // 2, paddle_width, paddle_height)
        else:
            self.rect = Rect(board.w - paddle_width * 2, board.centery - paddle_height // 2, paddle_width, paddle_height)

    def move(self):
        self.rect = self.rect.move(0, randint(-5, 5))
