from vector3f import Vector3f


class Ray:
    def __init__(self, origin: Vector3f, direction: Vector3f):
        self.origin = origin
        self.direction = direction.normalize()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__ + "({}, {})".format(self.origin, self.direction)