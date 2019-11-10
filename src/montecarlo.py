import math
import particleDataStructures
from vector2 import Vector2
from line import Line


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
    (nearest_wall, m) = find_nearest_wall(x, y, theta, mymap)
    print("nearest wall: ", nearest_wall)
    return likelihood(z, m, 0.03, 0.05)


# return (x0, y0, x1, y1)
def find_nearest_wall(x, y, theta, map):
    # loop through all the walls, calculate the distance m, and find which m is closest to the sonar measurement
    nearest_wall = None
    min_distance = math.inf

    for _wall in map.walls:
        wall = Line(Vector2(_wall[0], _wall[1]), Vector2(_wall[2], _wall[3]))
        m = calculate_forward_distance_to_wall(x, y, theta, wall)

        if m > 0 and m < min_distance:
            x_point_on_line = x + m * math.cos(math.radians(theta))
            y_point_on_line = y + m * math.sin(math.radians(theta))

            # check if distance actually goes through real wall, not wall of inf len
            if wall.bounds_point(Vector2(x_point_on_line, y_point_on_line)):
                min_distance = m
                nearest_wall = wall

    return (nearest_wall, min_distance)


# calculates m
def calculate_forward_distance_to_wall(x, y, theta, wall):
    Ax, Ay, Bx, By = wall.start_point.x, wall.start_point.y, wall.end_point.x, wall.end_point.y
    # uses var names from lecture slides so easier to implement
    denominator = (By - Ay) * math.cos(math.radians(theta)) - \
        (Bx - Ax) * math.sin(math.radians(theta))
    if denominator == 0:
        return math.inf

    numerator = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
    return numerator / denominator


def likelihood(z, m, sd, offset):
    exponent = (-((z - m) ** 2)) / (2 * sd * sd)
    return math.exp(exponent) + offset

# difference between wall normal and line made with sonar facing wall


def calculate_sonar_angle_to_wall(x, y, theta, wall):
    Ax, Ay, Bx, By = wall.start_point.x, wall.start_point.y, wall.end_point.x, wall.end_point.y

    numerator = math.cos(math.radians(theta)) * (Ay - By) + \
        math.sin(math.radians(theta)) * (Bx - Ax)
    denominator = math.sqrt((Ay - By) ** 2 + (Bx - Ax) ** 2)

    return math.degrees(math.acos(numerator/denominator))
