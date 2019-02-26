import math
from random import random

from rt8.material import color, Lambertian, Metal, Dielectric
from rt8.model import HitableList, Sphere
from rt8.camera import Camera
from vec3 import Vec3


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
    hitable_list.append(Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.8, 0.3, 0.3))))
    hitable_list.append(Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0))))
    hitable_list.append(Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), 0.1)))
    hitable_list.append(Sphere(Vec3(-1, 0, -1), 0.5, Dielectric(1.5)))
    hitable_list.append(Sphere(Vec3(-1, 0, -1), 0.45, Dielectric(1.5)))

    for i in range(ny - 1, -1, -1):
        for j in range(0, nx):
            col = Vec3(0, 0, 0)
            for s in range(ns):
                u = (j + random()) / nx
                v = (i + random()) / ny

                r = cam.get_ray(u, v)
                col += color(r, hitable_list, 0)

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