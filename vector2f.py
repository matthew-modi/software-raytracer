import math


class Vector2f:
    """Three element vector"""

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__ + "({}, {})".format(self.x, self.y)

    def __mul__(self, other):
        if isinstance(other, Vector2f):
            return Vector2f(self.x * other.x, self.y * other.y)
        else:
            return Vector2f(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Vector2f(self.x * other, self.y * other)

    def __add__(self, other):
        assert isinstance(other, Vector2f)
        return Vector2f(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Vector2f)
        return Vector2f(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):
        assert not isinstance(other, Vector2f)
        return Vector2f(self.x / other, self.y / other)

    def __neg__(self):
        return Vector2f(-self.x, -self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def normalize(self):
        return self / self.magnitude()

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def raw(self) -> list:
        return [self.x, self.y]
