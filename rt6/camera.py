from rt6.ray import Ray


class Camera(object):
    def __init__(self, origin, horizontal, vertical, lower_left_corner):
        self.origin = origin
        self.horizontal = horizontal
        self.vertical = vertical
        self.lower_left_corner = lower_left_corner

    def get_ray(self, u, v):
        return Ray(self.origin, self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)
