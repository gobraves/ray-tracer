import math

from rt2.ray import Ray
from vec3 import Vec3, dot, unit_vector


def hit_sphere(center: 'Vec3', radius: 'numbers.Real', ray: 'Ray'):
    oc = ray.origin - center

    a = dot(ray.direction, ray.direction)
    b = 2 * dot(oc, ray.direction)
    c = dot(oc, oc) - radius*radius
    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return -1
    else:
        return (-b - math.sqrt(discriminant)) / (2 * a)


def color(r: 'Ray'):
    t = hit_sphere(Vec3(0, 0, -1), 0.5, r)
    if t > 0:
        n = unit_vector(r.point_at_parameter(t) - Vec3(0, 0, -1))
        return 0.5*Vec3(n.x + 1, n.y + 1, n.z+1)
    unit_direction = unit_vector(r.direction)
    t = 0.5 * (unit_direction.y + 1)
    return (1-t) * Vec3(1, 1, 1) + t * Vec3(0.5, 0.7, 1)


def generate_ppm():
    nx = 400
    ny = 200

    pic_list = list()

    lower_left_corner = Vec3(-2, -1, -1)
    horizontal = Vec3(4, 0, 0)
    vertical = Vec3(0, 2, 0)
    origin = Vec3(0, 0, 0)

    for i in range(ny - 1, -1, -1):
        for j in range(0, nx):
            u = j / nx
            v = i / ny

            r = Ray(origin, lower_left_corner + u * horizontal + v * vertical)
            col = color(r)
            ir = int(255.99 * col.x)
            ig = int(255.99 * col.y)
            ib = int(255.99 * col.z)
            pic_list.append((ir, ig, ib))

    with open("pic.ppm", "w+") as f:
        f.write("P3\n")
        f.write("{} {}\n".format(nx, ny))
        f.write("255\n")
        for (ir, ig, ib) in pic_list:
            f.write("{} {} {}\n".format(ir, ig, ib))


if __name__=="__main__":
    generate_ppm()