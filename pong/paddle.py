from pygame import Rect


class Paddle:
    def __init__(self, left, board, player):

        self.controller = player
        paddle_height = 100
        paddle_width = 20

        if left:
            self.rect = Rect(paddle_width, board.centery - paddle_height // 2, paddle_width, paddle_height)
        else:
            self.rect = Rect(board.w - paddle_width * 2, board.centery - paddle_height // 2, paddle_width, paddle_height)

    def move(self, ball):
        self.rect = self.controller.take_move(self, ball)
