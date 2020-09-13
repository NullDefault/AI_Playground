from fosh.source.fish_components.fish_component import FishComponent
from pygame import Vector2


class Locomotion(FishComponent):
    def __init__(self, fish, loc):
        super().__init__(fish)
        self.angle = 0
        self.xy  = Vector2()  # XY Position
        self.xy.x, self.xy.y = loc[0], loc[1]
        self.dir = Vector2()  # Direction Vector
        self.acc = Vector2()  # Acceleration

