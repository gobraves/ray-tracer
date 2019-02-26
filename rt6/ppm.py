import sys
from random import randint, random

from rt6.ray import Ray
from rt6.model import Hitable, HitableList, Sphere
from rt6.camera import Camera
from vec3 import Vec3, unit_vector


def color(r: 'Ray', hitable: "Hitable") -> "Vec3":
    hit_record = hitable.hit(r, 0, sys.float_info.max)
    if hit_record:
        return 0.5 * (hit_record.normal + Vec3(1, 1, 1))

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

            ir = int(255.99 * col.x)
            ig = int(255.99 * col.y)
            ib = int(255.99 * col.z)
            pic_list.append((ir, ig, ib))

    with open("pic.ppm", "w+") as f:
        f.write("P3\n{} {}\n255\n".format(nx, ny))
        for (ir, ig, ib) in pic_list:
            f.write("{} {} {}\n".format(ir, ig, ib))


if __name__=="__main__":
    generate_ppm()