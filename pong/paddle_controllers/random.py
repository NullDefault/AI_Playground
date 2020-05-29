from random import randint


class Random:
    def take_move(self, paddle, ball):
        return paddle.rect.move(0, randint(-1, 1))
