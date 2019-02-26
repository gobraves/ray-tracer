import sys
from abc import abstractmethod
import random
from rt8.ray import Ray
from vec3 import *


class Material(object):
    @abstractmethod
    def scatter(self, r, hit_record):
        pass


class Lambertian(Material):
    def __init__(self, vec3):
        self.albedo = vec3

    def scatter(self, r, hit_record):
        target = hit_record.p + hit_record.normal + random_in_unit_sphere()
        scattered = Ray(hit_record.p, target - hit_record.p)
        attenuation = self.albedo

        return scattered, attenuation


class Metal(Material):
    def __init__(self, albedo, f):
        self.albedo = albedo
        self.fuzz = f if f < 1 else 1

    def scatter(self, r, hit_record):
        reflected = reflect(unit_vector(r.direction), hit_record.normal)
        scattered = Ray(hit_record.p, reflected + self.fuzz * random_in_unit_sphere())
        attenuation = self.albedo
        if dot(scattered.direction, hit_record.normal) > 0:
            return scattered, attenuation
        else:
            return None, None


class Dielectric(Material):
    def __init__(self, ri):
        self.ref_idx = ri

    def scatter(self, r, hit_record):
        reflected = reflect(r.direction, hit_record.normal)
        attenuation = Vec3(1, 1, 1)

        if dot(r.direction, hit_record.normal) > 0:
            outward_normal = -hit_record.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * dot(r.direction, hit_record.normal) / r.direction.length()
        else:
            outward_normal = hit_record.normal
            ni_over_nt = 1 / self.ref_idx
            cosine = -dot(r.direction, hit_record.normal) / r.direction.length()

        refracted = refract(r.direction, outward_normal, ni_over_nt)

        if refracted:
            reflect_prob = schlick(cosine, self.ref_idx)
        else:
            reflect_prob = 1

        if random.random() < reflect_prob:
            scattered = Ray(hit_record.p, reflected)
        else:
            scattered = Ray(hit_record.p, reflected)
        return scattered, attenuation


def color(r: 'Ray', hitable: "Hitable", depth: "int") -> "Vec3":
    hit_record = hitable.hit(r, 0.001, sys.float_info.max)
    if hit_record:
        scattered, attenuation = hit_record.material.scatter(r, hit_record)
        if depth < 50 and scattered is not None:
            return attenuation * color(scattered, hitable, depth + 1)
        else:
            return Vec3(0, 0, 0)
    else:
        unit_direction = unit_vector(r.direction)
        t = 0.5 * (unit_direction.y + 1)
        return (1 - t) * Vec3(1, 1, 1) + t * Vec3(0.5, 0.7, 1)


def random_in_unit_sphere():
    p = Vec3(1, 1, 1)
    while dot(p, p) > 1:
        a = random.uniform(0, 1)
        b = random.uniform(0, 1)
        c = random.uniform(0, 1)
        p = 2 * Vec3(a, b, c) - Vec3(1, 1, 1)
        if p.squared_length() < 1:
           return p


def refract(v: "Vec3", n: "Vec3", ni_over_nt: "float"):
    refracted = None
    uv = unit_vector(v)
    dt = dot(uv, n)
    discriminant = 1 - ni_over_nt * ni_over_nt * (1 - dt * dt)
    if discriminant > 0:
        refracted = ni_over_nt * (uv - n * dt) - n * math.sqrt(discriminant)
    return refracted


def schlick(cosine, ref_idx):
    r0 = (1-ref_idx) / (1+ref_idx)
    r0 = r0 * r0
    return r0 + (1-r0) * pow((1-cosine), 5)
