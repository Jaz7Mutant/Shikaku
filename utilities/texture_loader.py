from pyglet.gl import *
from pyglet.graphics import TextureGroup


def get_texture(filename: str) -> TextureGroup:
    img = pyglet.image.load(filename)
    texture = img.get_texture()
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    return pyglet.graphics.TextureGroup(texture)
