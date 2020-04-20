import tensorflow as tf


class QNAgent:
    def __init__(self, size):
        self.size = size
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(size**2))
        self.model.compile(optimizer='sgd', loss='mean_squared_error')
