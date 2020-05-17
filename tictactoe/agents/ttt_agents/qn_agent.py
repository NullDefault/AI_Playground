import tensorflow as tf
import numpy as np

from tictactoe.agents.ttt_agents.agent import Agent


class QNAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.last_move = None
        self.board_history = []
        self.q_history = []

        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(9))
        self.model.compile(optimizer='sgd', loss='mean_squared_error')

    def predict_q(self, board_cells):
        return self.model.predict(
            np.array([board_cells.ravel()])).reshape(3, 3)

    def fit_q(self, board_cells, q_values):
        self.model.fit(
            np.array([board_cells.ravel()]), np.array([q_values.ravel()]), verbose=0)

    def new_game(self):
        self.last_move = None
        self.board_history = []
        self.q_history = []

    def take_turn(self, board_data):
        board = board_data.cells

        q_values = self.predict_q(board)
        temp_q = q_values.copy()
        temp_q[board != -1] = temp_q.min() - 1  # no illegal moves
        move = np.unravel_index(np.argmax(temp_q), board.shape)
        value = temp_q.max()
        if self.last_move is not None:
            self.reward(value)
        self.board_history.append(board.copy())
        self.q_history.append(q_values)
        self.last_move = move
        return move

    def reward(self, reward_value):
        new_q = self.q_history[-1].copy()
        new_q[self.last_move] = reward_value
        self.fit_q(self.board_history[-1], new_q)
