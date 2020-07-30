from color import Color
from vector2f import Vector2f
from vector3f import Vector3f


class Triangle:
    def __init__(self, a: Vector3f, b: Vector3f, c: Vector3f, color: Color = Color(1.0, 1.0, 1.0), single_sided: bool = False):
        self.a = a
        self.b = b
        self.c = c
        self.normal = ((b - a).cross(c - a))
        self.area_sq = self.normal.magnitude()
        self.color = color
        self.single_sided = single_sided

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__ + "({}, {}, {}, {})".format(self.a, self.b, self.c, self.color)

    def intersect(self, ray) -> float:
        normal_dot = self.normal.dot(ray.direction)
        if abs(normal_dot) < 0.001:
            return -1.0

        if self.single_sided and normal_dot > 0:
            return -1.0

        d = self.normal.dot(self.a)
        t = (self.normal.dot(ray.origin) + d) / normal_dot

        p_hit = ray.origin + t * ray.direction

        if self.normal.dot((self.b - self.a).cross(p_hit - self.a)) < 0:
            return -1.0

        if self.normal.dot((self.c - self.b).cross(p_hit - self.b)) < 0:
            return -1.0

        if self.normal.dot((self.a - self.c).cross(p_hit - self.c)) < 0:
            return -1.0

        return t

    def get_surface_data(self, hit_pos):
        return {'normal': self.normal, 'texture': Vector2f()}
