class Ray(object):
    def __init__(self, origin: 'Vec3', direction: 'Vec3'):
        self.origin = origin
        self.direction = direction

    def point_at_parameter(self, parameter):
        return self.origin + parameter * self.direction
