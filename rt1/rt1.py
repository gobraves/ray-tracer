def generate_ppm():
    nx = 200
    ny = 100

    pic_list = list()

    for i in range(ny - 1, -1, -1):
        for j in range(0, nx):
            r = j / nx
            g = i / ny
            b = 0.2
            ir = int(255.99 * r)
            ig = int(255.99 * g)
            ib = int(255.99 * b)
            pic_list.append((ir, ig, ib))
    
    with open("/home/neo/rt/pic.ppm", "w+") as f:
        f.write("P3\n")
        f.write("{} {}\n".format(nx, ny))
        f.write("255\n")
        for (ir, ig, ib) in pic_list:
            f.write("{} {} {}\n".format(ir, ig, ib))

if __name__=="__main__":
    generate_ppm()
