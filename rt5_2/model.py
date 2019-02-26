import math
from abc import abstractmethod
from collections import namedtuple

from vec3 import dot

HitRecord = namedtuple("HitRecord", ["t", "p", "normal"])


class Hitable(object):
    @abstractmethod
    def hit(self, r: "Ray", t_min, t_max: "numbers.Real"):
        pass


class Sphere(Hitable):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def hit(self, ray: "Ray", t_min, t_max: "numbers.Real") -> "HitRecord/None":
        hit_record = None
        oc = ray.origin - self.center

        a = dot(ray.direction, ray.direction)
        b = 2 * dot(oc, ray.direction)
        c = dot(oc, oc) - self.radius ** 2
        discriminant = b * b - 4 * a * c

        if discriminant > 0:
            tmp_1 = (-b - math.sqrt(discriminant)) / (2*a)
            tmp_2 = (-b + math.sqrt(discriminant)) / (2*a)

            for tmp in [tmp_1, tmp_2]:
                if t_min < tmp < t_max:
                    p = ray.point_at_parameter(tmp)
                    normal = (p - self.center) / self.radius
                    hit_record = HitRecord(t=tmp, p=p, normal=normal)
                    break

        return hit_record


class HitableList(list, Hitable):

    def hit(self, r: "Ray", t_min, t_max: "numbers.Real") -> "HitRecord":
        final_hit_record = None
        tmp_t_max = t_max

        for i in self:
            hit_record = i.hit(r, t_min, tmp_t_max)
            if hit_record:
                tmp_t_max = hit_record.t
                final_hit_record = hit_record

        if final_hit_record:
            return final_hit_record


