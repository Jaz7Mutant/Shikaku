from copy import deepcopy

import pyglet

from Utilities.point import Point


class Square:
    def __init__(self, number: str, point1: Point, point2: Point, color):
        self.cords = [
            point1.x, point1.y,
            point2.x, point1.y,
            point2.x, point2.y,
            point1.x, point2.y
        ]
        self.color = deepcopy(color)
        self.label = pyglet.text.Label(
            number,
            font_name='Arial',
            font_size=20,
            color=(0, 0, 0, 255),
            x=(point1.x+point2.x)//2,
            y=(point1.y+point2.y)//2,
            anchor_x='center', anchor_y='center')

    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', self.cords),
                             ('c3B', self.color * int(len(self.cords)/2)))
        self.label.draw()
