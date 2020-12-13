from pygame import Color

WIDTH, HEIGHT = 1280, 920
SIZES = {
    'small': [50, 10, 6],
    'medium': [100, 5, 3],
    'large': [125, 4, 2.4],
    'too big': [250, 2, 1.2]
}

COLORS = {
    'fox':    Color(255, 150, 50),
    'rabbit': Color(50, 25, 0),
    'brown':  Color(150, 100, 45),
    'grass_colors': {
        0: Color(230, 255, 240),
        1: Color(200, 255, 200),
        2: Color(145, 255, 110),
        3: Color(100, 255, 80),
        4: Color(60, 255, 40),
        5: Color(40, 255, 20),
        6: Color(15, 255, 10)
    }
}