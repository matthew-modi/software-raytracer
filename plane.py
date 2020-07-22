import math

from color import Color
from vector2f import Vector2f
from vector3f import Vector3f
import numpy as np


class Plane:
    def __init__(self, center: Vector3f, normal: Vector3f, color: Color = Color(1.0, 1.0, 1.0)):
        self.center = center
        self.normal = normal.normalize()
        self.color = color

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__ + "({}, {}, {})".format(self.center, self.normal, self.color)

    def intersect(self, ray) -> float:
        denominator = self.normal.dot(ray.direction)
        if abs(denominator) > 0.0:
            t = (self.center - ray.origin).dot(self.normal)/denominator
            return t
        return -1.0

    def get_surface_data(self, hit_pos):
        return {'normal': self.normal, 'texture': Vector2f(hit_pos.x/4, hit_pos.z/4)}
    #Vector2f((1 + math.atan2(normal.z, normal.x) / math.pi) * 0.5, math.acos(normal.y) / math.pi)
