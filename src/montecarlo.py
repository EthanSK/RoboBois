import math
import particleDataStructures


def generate_map():
    mymap = particleDataStructures.Map()
    # Definitions of walls
    # a: O to A
    # b: A to B
    # c: C to D
    # d: D to E
    # e: E to F
    # f: F to G
    # g: G to H
    # h: H to O
    mymap.add_wall((0, 0, 0, 168))        # a
    mymap.add_wall((0, 168, 84, 168))     # b
    mymap.add_wall((84, 126, 84, 210))    # c
    mymap.add_wall((84, 210, 168, 210))   # d
    mymap.add_wall((168, 210, 168, 84))   # e
    mymap.add_wall((168, 84, 210, 84))    # f
    mymap.add_wall((210, 84, 210, 0))     # g
    mymap.add_wall((210, 0, 0, 0))        # h
    return mymap


def calculate_likelihood(x, y, theta, z):
    mymap = generate_map()
    nearest_wall = find_nearest_wall(x, y, theta, z, mymap)
    m = calculate_distance_to_wall(x, y, theta, nearest_wall)
    return likelihood(z, m, 0.03, 0.05)


# return (x0, y0, x1, y1)
def find_nearest_wall(x, y, theta, z, map):
    # loop through all the walls, calculate the distance m, and find which m is closest to the sonar measurement
    min_distance = float("inf")
    for wall in map.walls:
        distance = calculate_distance_to_wall(x, y, theta, wall)
        if distance < min_distance:
            min_distance = distance
            nearest_wall = wall
    return nearest_wall


# calculates m
def calculate_distance_to_wall(x, y, theta, wall):
    Ax, Ay, Bx, By = wall[0], wall[1], wall[2], wall[3]
    numerator = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
    denomenator = (By - Ay) * math.cos(theta) - (Bx - Ax) * math.sin(theta)
    return numerator/denomenator


def likelihood(z, m, sd, offset):
    exponent = (-((z - m) ** 2)) / (2 * sd * sd)
    return math.exp(exponent) + offset
