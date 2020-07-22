import colorsys
import math


class Color:
    """RGB color object"""

    def __init__(self, a: float = 0.0, b: float = 0.0, c: float = 0.0, type: str = 'rgb'):
        if type == 'rgb':
            self.r = a
            self.g = b
            self.b = c
        elif type == 'hsv':
            rgb = colorsys.hsv_to_rgb(a, b, c)
            self.r = rgb[0]
            self.g = rgb[1]
            self.b = rgb[2]


    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__ + "({}, {}, {})".format(self.r, self.g, self.b)

    def __mul__(self, other):
        assert not isinstance(other, Color)
        return Color(self.r * other, self.g * other, self.b * other)

    def __rmul__(self, other):
        assert isinstance(other, float)
        return Color(self.r * other, self.g * other, self.b * other)

    def raw(self) -> list:
        return [self.r, self.g, self.b]
