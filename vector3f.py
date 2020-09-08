import math

import numpy


class Vector3f:
    """Three element vector"""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__ + "<{}, {}, {}>".format(self.x, self.y, self.z)

    def __mul__(self, other):
        if isinstance(other, Vector3f):
            return Vector3f(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vector3f(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return Vector3f(self.x * other, self.y * other, self.z * other)

    def __add__(self, other):
        assert isinstance(other, Vector3f)
        return Vector3f(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        assert isinstance(other, Vector3f)
        return Vector3f(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, other):
        assert not isinstance(other, Vector3f)
        return Vector3f(self.x / other, self.y / other, self.z / other)

    def __neg__(self):
        return Vector3f(-self.x, -self.y, -self.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3f(self.y * other.z - self.z * other.y,
                        self.z * other.x - self.x * other.z,
                        self.x * other.y - self.y * other.x)

    def normalize(self):
        return self / self.magnitude()

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def raw(self) -> list:
        return [self.x, self.y, self.z]
