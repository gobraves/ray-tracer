import math
import numbers


class Vec3(object):
    def __init__(self, e0, e1, e2):
        self.e = (e0, e1, e2)

    @property
    def x(self):
        return self.e[0]

    @property
    def y(self):
        return self.e[1]

    @property
    def z(self):
        return self.e[2]

    @property
    def r(self):
        return self.e[0]

    @property
    def g(self):
        return self.e[1]

    @property
    def b(self):
        return self.e[2]

    def __add__(self, other):
        return Vec3(*[e1 + e2 for (e1, e2) in zip(self.e, other.e)])

    def __radd__(self, other):
        return Vec3(*[e1 + e2 for (e1, e2) in zip(self.e, other.e)])

    def __iadd__(self, other):
        return Vec3(*[e1 + e2 for (e1, e2) in zip(self.e, other.e)])

    def __sub__(self, other):
        return Vec3(*[e1 - e2 for (e1, e2) in zip(self.e, other.e)])

    def __sub__(self, other):
        return Vec3(*[e1 - e2 for (e1, e2) in zip(self.e, other.e)])

    def __neg__(self):
        return Vec3(*(-self.e[0], -self.e[1], -self.e[2]))

    def __isub__(self, other):
        return Vec3(*[e1 - e2 for (e1, e2) in zip(self.e, other.e)])

    def __rmul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(*[e1 * e2 for (e1, e2) in zip(self.e, other.e)])
        if isinstance(other, numbers.Real):
            return Vec3(*[other * i for i in self.e])

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(*[e1 * e2 for (e1, e2) in zip(self.e, other.e)])
        if isinstance(other, numbers.Real):
            return Vec3(*[other * i for i in self.e])

    def __imul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(*[e1 * e2 for (e1, e2) in zip(self.e, other.e)])
        elif isinstance(other, numbers.Real):
            return Vec3(*[other * i for i in self.e])

    def __truediv__(self, other):
        if isinstance(other, Vec3):
            return Vec3(*[e1 / e2 for (e1, e2) in zip(self.e, other.e)])
        elif isinstance(other, numbers.Real):
            return Vec3(*[i / other for i in self.e])

    def __itruediv__(self, other):
        if isinstance(other, Vec3):
            return Vec3(*[e1 / e2 for (e1, e2) in zip(self.e, other.e)])
        elif isinstance(other, numbers.Real):
            return Vec3(*[i / other for i in self.e])

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def squared_length(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def __repr__(self):
        return '{} {} {}'.format(self.r, self.g, self.b)


def unit_vector(vec3):
    return vec3 / vec3.length()


def dot(vec3, other):
    return sum([e1 * e2 for (e1, e2) in zip(vec3.e, other.e)])


def cross(vec3, other):
    return Vec3(
        vec3.y * other.z - vec3.z * other.y,
        vec3.z * other.x - vec3.x * other.z,
        vec3.x * other.y - vec3.y * other.x
    )


def reflect(v: "Vec3", n: "Vec3"):
    return v - 2 * dot(v, n) * n
