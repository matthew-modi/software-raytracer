import math

from color import Color
from vector2f import Vector2f
from vector3f import Vector3f
import numpy as np


class Sphere:
    def __init__(self, center: Vector3f, radius: float, color: Color = Color(1.0, 1.0, 1.0)):
        self.center = center
        self.radius = radius
        self.radius_sq = radius ** 2
        self.color = color

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__ + "({}, {}, {})".format(self.center, self.radius, self.color)

    def intersect(self, ray) -> float:
        distance = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(distance)
        c = distance.dot(distance) - self.radius_sq
        roots = [root for root in np.roots([a, b, c]) if not isinstance(root, complex) and root > 0.0]

        if len(roots) == 0:
            return -1.0
        roots = sorted(roots)
        return roots[0]

    def get_surface_data(self, hit_pos):
        normal = (hit_pos - self.center).normalize()
        return {'normal': normal, 'texture': Vector2f((1 + math.atan2(normal.z, normal.x) / math.pi) * 0.5, math.acos(normal.y) / math.pi)}

