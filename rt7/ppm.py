import sys
import math
from random import randint, random

from rt7.ray import Ray
from rt7.model import Hitable, HitableList, Sphere
from rt7.camera import Camera
from vec3 import Vec3, unit_vector, dot


def random_in_unit_sphere():
    p = Vec3(1.0, 1.0, 1.0)
    while dot(p, p) > 1:
        a = random()
        b = random()
        c = random()
        p = 2 * Vec3(a, b, c) - Vec3(1, 1, 1)
    return p


def color(r: 'Ray', hitable: "Hitable") -> "Vec3":
    hit_record = hitable.hit(r, 0, sys.float_info.max)
    if hit_record:
        target = hit_record.p + hit_record.normal + random_in_unit_sphere()
        return 0.5 * color(Ray(hit_record.p, target - hit_record.p), hitable)

    unit_direction = unit_vector(r.direction)
    t = 0.5 * (unit_direction.y + 1)
    return (1-t) * Vec3(1, 1, 1) + t * Vec3(0.5, 0.7, 1)


def generate_ppm():
    nx = 200
    ny = 100

    ns = 100

    pic_list = list()

    lower_left_corner = Vec3(-2, -1, -1)
    horizontal = Vec3(4, 0, 0)
    vertical = Vec3(0, 2, 0)
    origin = Vec3(0, 0, 0)

    cam = Camera(origin, horizontal, vertical, lower_left_corner)

    hitable_list = HitableList()
    hitable_list.append(Sphere(Vec3(0, 0, -1), 0.5))
    hitable_list.append(Sphere(Vec3(0, -100.5, -1), 100))

    for i in range(ny - 1, -1, -1):
        for j in range(0, nx):
            col = Vec3(0, 0, 0)
            for s in range(ns):
                u = (j + random()) / nx
                v = (i + random()) / ny

                r = cam.get_ray(u, v)
                col += color(r, hitable_list)

            col /= ns

            ir = int(255.99 * math.sqrt(col.x))
            ig = int(255.99 * math.sqrt(col.y))
            ib = int(255.99 * math.sqrt(col.z))
            pic_list.append((ir, ig, ib))

    with open("pic.ppm", "w+") as f:
        f.write("P3\n{} {}\n255\n".format(nx, ny))
        for (ir, ig, ib) in pic_list:
            f.write("{} {} {}\n".format(ir, ig, ib))


if __name__=="__main__":
    generate_ppm()