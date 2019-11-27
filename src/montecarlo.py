import math
import particleDataStructures
from vector2 import Vector2
from line import Line
import map_data


MAX_ANGLE = 45


def draw_lines():
    mymap = map_data.generate_map()
    mymap.draw()


def calculate_likelihood(x, y, theta, z):
    mymap = map_data.generate_map()
    (nearest_wall, m) = find_nearest_wall(x, y, theta, mymap)
    # print("nearest wall: ", chr(65 + mymap.walls.index((nearest_wall.start_point.x, nearest_wall.start_point.y, nearest_wall.end_point.x, nearest_wall.end_point.y))))
    return likelihood(z, m, 3, 0.00001)


# return (x0, y0, x1, y1)
def find_nearest_wall(x, y, theta, map):
    # loop through all the walls, calculate the distance m, and find which m is closest to the sonar measurement
    nearest_wall = None
    min_distance = math.inf
    walls_as_lines = map.convert_walls_to_lines()
    for wall in walls_as_lines:
        m = calculate_forward_distance_to_wall(x, y, theta, wall)

        # and calculate_forward_angle_to_wall(x, y, theta, wall) < MAX_ANGLE:
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
    exponent = (-((z - m) ** 2)) / (2 * sd ** 2)
    return (math.exp(exponent) + offset) * 10000

# difference between wall normal and line made with sonar facing wall


def calculate_forward_angle_to_wall(x, y, theta, wall):
    Ax, Ay, Bx, By = wall.start_point.x, wall.start_point.y, wall.end_point.x, wall.end_point.y

    numerator = math.cos(math.radians(theta)) * (Ay - By) + \
        math.sin(math.radians(theta)) * (Bx - Ax)
    denominator = math.sqrt((Ay - By) ** 2 + (Bx - Ax) ** 2)

    return math.degrees(math.acos(numerator/denominator))
