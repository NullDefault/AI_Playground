class AimBot:
    def take_move(self, paddle, ball):
        paddle_center = paddle.rect.top + paddle.rect.h // 2
        y_diff = ball.pos[1] - paddle_center
        if y_diff > 0:
            return paddle.rect.move(0, 1)
        else:
            return paddle.rect.move(0, -1)