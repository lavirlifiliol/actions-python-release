import random
from math import sin, cos, pi, sqrt, e, radians

import arcade

# Do the math to figure out our screen dimensions
WIDTH = 800
HEIGHT = 800
TITLE = "hex grid"
SIZE = 10.0


def hex_v(x, y, i, size=SIZE):
    a = pi / 3 * i
    return x + cos(a) * size, y + sin(a) * size


def tocube(a):
    q, r = a
    return q, r, -q - r


def round_qr(a):
    cube = list(tocube(a))
    l, m, n = map(round, cube)
    i, j, k = cube
    diffi = abs(l - i)
    diffj = abs(m - j)
    diffk = abs(n - k)
    if diffk < diffi > diffj:
        return -m - n, m
    elif diffi > diffj:
        return l, -l - n
    else:
        return l, m


def qr_to_xy(a, size=SIZE):
    q, r = a
    x = 3 / 2 * q * size
    y = (sqrt(3) / 2 * q + sqrt(3) * r) * size
    return x, y


def dist(a, b):
    i, j, k = tocube(a)
    l, m, n = tocube(b)
    return (abs(i - l) + abs(j - m) + abs(k - n)) // 2


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        """
        Set up the application.
        """
        super().__init__(WIDTH, HEIGHT, TITLE)

        self.sizes = [15 + i / 5 for i in range(-5, 6)]
        self.i = len(self.sizes) - 1
        self.sd = 1
        self.level = 0
        self.hi = 0
        self.shape_lists = [arcade.ShapeElementList() for _ in self.sizes]
        self.coords = []
        self.press = None
        s = 12
        for q in range(-s, s + 1):
            for r in range(-s, s + 1):
                if dist((q, r), (0, 0)) <= s:
                    self.coords.append((q, r))
                    for i, size in enumerate(self.sizes):
                        x, y = qr_to_xy((q, r), size)
                        color = arcade.color.KOBE
                        points = [hex_v(x, y, i, size) for i in range(7)]

                        line = arcade.create_line_strip(points, color, 2)
                        self.shape_lists[i].append(line)

        for sl in self.shape_lists:
            sl.center_x = WIDTH // 2
            sl.center_y = HEIGHT // 2
            sl.angle = 0
        self.target = random.choice(self.coords)

        self.decoys = None
        self.reroll_decoys()
        arcade.set_background_color(arcade.color.BLACK)

    def highlight(self, qr, color=arcade.color.ANDROID_GREEN):
        size = self.sizes[self.i]
        x, y = qr_to_xy(qr, size)
        c = (x + y * 1j) * (e ** (radians(self.shape_lists[0].angle) * 1j))
        x = c.real + WIDTH // 2
        y = c.imag + HEIGHT // 2
        arcade.draw_circle_filled(x, y, size * 0.7, color)

    def reroll_decoys(self):
        self.decoys =[d for d in random.choices(self.coords, k=self.level * 4) if d != self.target]

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        for decoy in self.decoys:
            self.highlight(decoy, arcade.color.ALIZARIN_CRIMSON)
        self.highlight(self.target)
        arcade.draw_text(f'Score: {self.level} Hi: {self.hi}', 10, 10, arcade.color.GHOST_WHITE, font_size=20)

        self.shape_lists[self.i].draw()

    def on_update(self, delta_time):
        for sl in self.shape_lists:
            sl.angle += self.level / 10

        if self.level > 9:
            if not 0 <= self.i + self.sd < len(self.sizes):
                self.i += self.sd
                self.sd *= -1
            self.i += self.sd

    def on_mouse_press(self, ox: float, oy: float, button: int, modifiers: int):
        ox -= WIDTH // 2
        oy -= HEIGHT // 2
        c = (ox + oy * 1j) * (e ** -(radians(self.shape_lists[0].angle) * 1j))
        x = c.real
        y = c.imag
        size = self.sizes[self.i]
        q = (2 / 3 * x) / size
        r = (-1 / 3 * x + sqrt(3) / 3 * y) / size
        hit = round_qr((q, r))
        if self.target == hit:
            self.target = random.choice(self.coords)
            self.level += 1
            self.reroll_decoys()
        elif hit in self.decoys:
            self.hi = max(self.hi, self.level)
            self.level = 0
            self.target = random.choice(self.coords)
            self.reroll_decoys()
            self.i = len(self.sizes) - 1

def main():
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
