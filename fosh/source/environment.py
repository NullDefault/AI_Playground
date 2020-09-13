class Environment:
    def __init__(self, w, h):
        self.floor_coords = ([0, h], [w, h], [w - 200, h - 200], [200, h - 200])
        self.l_wall = ([0, h], [0, 200], [200, 0], [200, h-200])
        self.r_wall = ([w, h], [w, 200], [w-200, 0], [w-200, h-200])
        self.b_wall = ([200, 0], [200, h-200], [w-200, h-200], [w-200, 0])
        self.f_panel = ([0, 200], [0, h], [w, h], [w, 200])
        self.water = ([0, 300], [200, 100], [w - 200, 100], [w, 300], [w, h], [0, h])
        self.water_cap = ([0, 300], [200, 100], [w-200, 100], [w, 300])

