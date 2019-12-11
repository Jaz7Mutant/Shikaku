import math
from pyglet.gl import *

from Utilities.texture_loader import get_texture


class InteractiveField:
    def __init__(self, filename, x1, y1, z1, x2, y2, z2):
        self.filename = filename
        self.texture = get_texture(filename)
        self.first_point = (x1, y1, z1)
        self.second_point = (x2, y2, z2)
        self.batch = pyglet.graphics.Batch()
        self.side = self.batch.add(
            4,
            GL_QUADS,
            self.texture,
            ('v3f', (x2, y1, z1, x2, y2, z1, x1, y2, z1, x1, y1, z1)),
            ('t2f/dynamic',
             (1, 0, 1, 1, 0, 1, 0, 0)))

    def restart(self):
        self.texture = get_texture(self.filename)
        self.batch = pyglet.graphics.Batch()
        self.side = self.batch.add(
            4,
            GL_QUADS,
            self.texture,
            ('v3f', (self.second_point[0], self.first_point[1],
                     self.first_point[2], self.second_point[0],
                     self.second_point[1], self.first_point[2],
                     self.first_point[0], self.second_point[1],
                     self.first_point[2], self.first_point[0],
                     self.first_point[1], self.first_point[2])),
            ('t2f/dynamic',
             (1, 0, 1, 1, 0, 1, 0, 0)))

    def draw(self):
        self.batch.draw()

    def check_intersection(self, player_pos) -> bool:
        return self.second_point[0] + 0.2 > player_pos[0] > self.first_point[0] - 0.2 and \
               self.second_point[1] + 0.3 > player_pos[1] > self.first_point[1] - 0.3 and \
               self.second_point[2] + 0.3 > player_pos[2] > self.first_point[2] - 0.3

    def get_player_pos(self):
        x = (self.first_point[0] + self.second_point[0]) / 2
        y = (self.first_point[1] + self.second_point[1]) / 2
        z = (self.first_point[2] + self.second_point[2]) / 2
        return [x, y, z + 2]
