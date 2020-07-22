import math

from color import Color
from vector2f import Vector2f
from vector3f import Vector3f


class Box:
    def __init__(self, min: Vector3f, max: Vector3f, color: Color = Color(1.0, 1.0, 1.0)):
        self.min = min
        self.max = max
        self.color = color

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__ + "({}, {}, {})".format(self.min, self.max, self.color)

    def intersect(self, ray) -> float:
        t_min = (self.min.x - ray.origin.x) / ray.direction.x
        t_max = (self.max.x - ray.origin.x) / ray.direction.x

        if t_min > t_max:
            t_min, t_max = t_max, t_min
        
        t_min_y = (self.min.y - ray.origin.y) / ray.direction.y
        t_max_y = (self.max.y - ray.origin.y) / ray.direction.y
        
        if t_min_y > t_max_y:
            t_min_y, t_max_y = t_max_y, t_min_y
            
        if t_min > t_max_y or t_min_y > t_max:
            return -1.0
        
        if t_min_y > t_min:
            t_max = t_max_y

        t_min_z = (self.min.z - ray.origin.z) / ray.direction.z
        t_max_z = (self.max.z - ray.origin.z) / ray.direction.z

        if t_min_z > t_max_z:
            t_min_z, t_max_z = t_max_z, t_min_z

        if t_min > t_max_z or t_min_z > t_max:
            return -1.0

        return 0.000001

    def get_surface_data(self, hit_pos):
        return {'normal': Vector3f(), 'texture': Vector2f()}

