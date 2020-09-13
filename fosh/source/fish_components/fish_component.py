from abc import ABC


class FishComponent(ABC):
    def __init__(self, fish):
        self.host = fish
